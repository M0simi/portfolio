from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .models import Event, FAQ, CustomUser, KnowledgeBase
from .serializers import EventSerializer, FAQSerializer, UserSerializer
from .ai_service import ask_gemini

from PyPDF2 import PdfReader
import requests
from io import BytesIO


# ✅ تسجيل الدخول (باستخدام البريد)
class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'يجب إدخال البريد وكلمة المرور.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)
        if not user:
            return Response({'error': 'بيانات الدخول غير صحيحة.'}, status=status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': str(user.pk),
            'email': user.email,
            'name': user.name,
            'role': user.role,
        })


# ✅ عرض الأحداث (قائمة) مع فلاتر status و q
@api_view(['GET'])
@permission_classes([AllowAny])
def get_events(request):
    """
    - status=upcoming | past | all (افتراضي all)
    - q=بحث بالعنوان أو الوصف
    """
    qs = Event.objects.all()
    now = timezone.now()

    # فلتر حسب الحالة
    status_param = (request.GET.get('status') or '').lower()
    if status_param == 'upcoming':
        # يبدأ الآن أو لاحقًا
        qs = qs.filter(start_date__gte=now)
    elif status_param == 'past':
        # انتهى: (له end_date وانتهى) أو (بدون end_date لكنه بدأ قبل الآن)
        qs = qs.filter(Q(end_date__lt=now) | Q(end_date__isnull=True, start_date__lt=now))
    # else: all

    # فلتر البحث
    q = request.GET.get('q')
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))

    qs = qs.order_by('start_date')
    serializer = EventSerializer(qs, many=True, context={'request': request})
    return Response(serializer.data)


# ✅ تفاصيل حدث بالـ slug (مفتوح للجميع)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_event_detail(request, slug):
    try:
        event = Event.objects.get(slug=slug)
    except Event.DoesNotExist:
        return Response({'detail': 'الحدث غير موجود'}, status=status.HTTP_404_NOT_FOUND)
    serializer = EventSerializer(event, context={'request': request})
    return Response(serializer.data)


# ✅ البحث في الأسئلة
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def search_faqs(request):
    query = request.data.get('query', '')
    faqs = FAQ.objects.filter(question__icontains=query)[:5]
    serializer = FAQSerializer(faqs, many=True)
    return Response({'results': serializer.data})


# ✅ الصفحة الرئيسية للـ API
@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        'message': '🎓 مرحباً بك في UniBot API',
        'endpoints': {
            'register': 'POST /api/register/',
            'login': 'POST /api/login/',
            'events': 'GET /api/events/',
            'event_detail': 'GET /api/events/<slug>/',  # تمت إضافة التفاصيل
            'search': 'POST /api/search/',
            'ai_general': 'POST /api/ai/general/',
        },
        'status': '✅ API جاهز للعمل'
    })


# ✅ تسجيل مستخدم جديد
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    name = request.data.get('name')
    email = request.data.get('email')
    password = request.data.get('password')
    role = request.data.get('role', 'student')

    if not all([email, password]):
        return Response({'error': 'الرجاء إدخال البريد وكلمة المرور.'}, status=status.HTTP_400_BAD_REQUEST)

    if CustomUser.objects.filter(email=email).exists():
        return Response({'error': 'البريد الإلكتروني مستخدم مسبقاً.'}, status=status.HTTP_400_BAD_REQUEST)

    user = CustomUser.objects.create(
        name=name or "",
        email=email,
        password=make_password(password),
        role=role
    )

    serializer = UserSerializer(user)
    token, _ = Token.objects.get_or_create(user=user)

    return Response({
        'message': 'تم إنشاء الحساب بنجاح 🎉',
        'user': serializer.data,
        'token': token.key
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ai_general(request):
    user = request.user
    user_prompt = (request.data.get('prompt') or '').strip()
    if not user_prompt:
        return Response({'error': 'يرجى إدخال السؤال.'}, status=status.HTTP_400_BAD_REQUEST)

    # آخر ملف قاعدة معرفة
    kb = KnowledgeBase.objects.order_by('-id').first()
    if not kb or not kb.file:
        return Response({'error': '⚠️ لا يوجد ملف قاعدة معرفة مرفوع بعد.'}, status=status.HTTP_404_NOT_FOUND)

    pdf_text = ""
    try:
        # 1) لو التخزين محلي وفيه path صالح
        try:
            pdf_path = kb.file.path  # ممكن يرفع استثناء مع Cloudinary
            with open(pdf_path, "rb") as f:
                reader = PdfReader(f)
                for page in reader.pages:
                    content = page.extract_text() or ""
                    if content:
                        pdf_text += content + "\n"
        except Exception:
            # 2) تخزين سحابي (Cloudinary) — نقرأ من URL
            file_url = kb.file.url  # public URL
            r = requests.get(file_url, timeout=15)
            r.raise_for_status()
            reader = PdfReader(BytesIO(r.content))
            for page in reader.pages:
                content = page.extract_text() or ""
                if content:
                    pdf_text += content + "\n"

    except Exception as e:
        return Response({'error': f'⚠️ خطأ أثناء قراءة الملف: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    name = user.name or "الطالب"
    greetings = ["السلام عليكم", "مرحبا", "هلا", "صباح الخير", "مساء الخير", "أهلاً", "هلا والله"]
    if any(g in user_prompt for g in greetings):
        return Response({'result': f"وعليكم السلام {name}! 👋 كيف أقدر أساعدك اليوم؟"})

    full_prompt = f"""
    أنت UniBot 🎓 — مساعد جامعي عربي.
    أجب اعتمادًا فقط على النص التالي المقتبس من دليل الجامعة.
    إذا لم تجد إجابة مباشرة في النص، جاوب: "عذرًا، سؤالك غير موجود في الملف الحالي."

    --- نص الدليل (مقتطف) ---
    {pdf_text[:6000]}

    --- سؤال المستخدم ({name}) ---
    {user_prompt}
    """

    try:
        answer = ask_gemini(full_prompt).strip()
        clean = (answer.replace("حسب الملف", "")
                        .replace("وفقًا للمستند", "")
                        .replace("PDF", "")
                        .replace("الملف", "")
                        .strip())
        if any(w in clean for w in ["غير واضح", "لا أعلم", "لا يمكنني", "غير موجود"]):
            clean = "عذرًا، سؤالك غير موجود في الملف الحالي."
        return Response({'result': clean})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ✅ الملف الشخصي
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    user = request.user

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = request.data
        user.name = data.get('name', user.name)
        user.role = data.get('role', user.role)
        user.save()
        serializer = UserSerializer(user)
        return Response({
            'message': '✅ تم تحديث الملف الشخصي بنجاح',
            'user': serializer.data
        })




