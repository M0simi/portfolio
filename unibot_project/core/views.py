from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from .models import Event, FAQ, CustomUser
from .serializers import EventSerializer, FAQSerializer, UserSerializer
from .ai_service import ask_gemini
import os
from PyPDF2 import PdfReader
from core.models import KnowledgeBase

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


# ✅ عرض جميع الأحداث (مفتوح للجميع)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_events(request):
    events = Event.objects.all().order_by('start_date')
    serializer = EventSerializer(events, many=True)
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
    user_prompt = request.data.get('prompt', '').strip()

    if not user_prompt:
        return Response({'error': 'يرجى إدخال السؤال.'}, status=status.HTTP_400_BAD_REQUEST)

    # 🔹 قراءة آخر ملف PDF مرفوع من لوحة التحكم
    kb = KnowledgeBase.objects.order_by('-id').first()
    if not kb or not kb.file:
        return Response({'error': '⚠️ لا يوجد ملف قاعدة معرفة مرفوع بعد.'}, status=status.HTTP_404_NOT_FOUND)

    pdf_path = kb.file.path
    pdf_text = ""
    try:
        with open(pdf_path, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                content = page.extract_text()
                if content:
                    pdf_text += content + "\n"
    except Exception as e:
        return Response({'error': f'⚠️ خطأ أثناء قراءة الملف: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 👤 اسم المستخدم
    name = user.name or "الطالب"

    # 🧠 فلترة الأسئلة غير الأكاديمية
    arabic_letters = sum(1 for c in user_prompt if '\u0600' <= c <= '\u06FF')
    if arabic_letters < len(user_prompt) * 0.3:
        return Response({
            'result': f"عذرًا {name}، هذا السؤال لا يبدو أكاديميًا. حاول طرح سؤال متعلق بالجامعة 🎓"
        })

    # 🎯 إعداد البرومبت الذكي
    full_prompt = f"""
    أنت UniBot 🎓 — مساعد جامعي ذكي ناطق بالعربية الفصحى.
    تحدث مع {name} بأسلوب لبق وأكاديمي كما يفعل مرشد جامعي رسمي.
    أجب بدقة ووضوح وبشكل مختصر دون استخدام العامية.
    استعن بالمحتوى التالي من دليل الأسئلة الجامعية إن احتوى على الإجابة، ولكن لا تذكر أنك استخدمته:
    
    🔹 دليل الأسئلة الجامعية:
    {pdf_text[:6000]}
    
    🔹 سؤال {name}:
    {user_prompt}

    أجب إجابة أكاديمية فصيحة ومنظمة، تبدأ بتحية بسيطة مثل "أهلاً {name}" أو "مرحباً {name}".
    لا تذكر أنك تعتمد على ملف أو ذكاء اصطناعي أو مصدر.
    """

    try:
        answer = ask_gemini(full_prompt)
        clean_answer = (
            answer.replace("حسب الملف", "")
                  .replace("وفقًا للمستند", "")
                  .replace("PDF", "")
                  .replace("الملف", "")
                  .strip()
        )
        return Response({'result': clean_answer})
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
