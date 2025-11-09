# core/views.py
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

from .models import Event, FAQ, CustomUser
from .serializers import EventSerializer, FAQSerializer, UserSerializer
from .ai_service import ask_gemini

# (اختياري) فحص النماذج المتاحة من Gemini
import google.generativeai as genai
import re


def _clean_text(s: str) -> str:
    """تنظيف بسيط لنصوص الإدخال (مسافات + محارف غير مرئية)."""
    if not s:
        return ""
    s = re.sub(r"[\u200c\u200d\u200e\u200f]", "", s)  # ZWJ/ZWNJ/RTL marks
    return s.strip()


# =========================
# تسجيل الدخول (بالبريد)
# =========================
class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = _clean_text(request.data.get('email'))
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'يجب إدخال البريد وكلمة المرور.'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)
        if not user:
            return Response({'error': 'بيانات الدخول غير صحيحة.'},
                            status=status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': str(user.pk),
            'email': user.email,
            'name': user.name,
            'role': user.role,
        })


# =========================
# الأحداث
# =========================
@api_view(['GET'])
@permission_classes([AllowAny])
def get_events(request):
    """
    بارامترات اختيارية:
    - status = upcoming | past | all (افتراضي all)
    - q      = بحث بالعنوان أو الوصف
    """
    qs = Event.objects.all()
    now = timezone.now()

    status_param = (request.GET.get('status') or '').lower().strip()
    if status_param == 'upcoming':
        qs = qs.filter(start_date__gte=now)
    elif status_param == 'past':
        qs = qs.filter(Q(end_date__lt=now) | Q(end_date__isnull=True, start_date__lt=now))
    # else: all

    q = _clean_text(request.GET.get('q'))
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))

    qs = qs.order_by('start_date')
    serializer = EventSerializer(qs, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_event_detail(request, slug):
    try:
        event = Event.objects.get(slug=slug)
    except Event.DoesNotExist:
        return Response({'detail': 'الحدث غير موجود'}, status=status.HTTP_404_NOT_FOUND)
    serializer = EventSerializer(event, context={'request': request})
    return Response(serializer.data)


# =========================
# البحث في الأسئلة الشائعة
# =========================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def search_faqs(request):
    query = _clean_text(request.data.get('query'))
    faqs = FAQ.objects.filter(question__icontains=query)[:5] if query else []
    serializer = FAQSerializer(faqs, many=True)
    return Response({'results': serializer.data})


# =========================
# الجذر التعريفي للـ API
# =========================
@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        'message': '🎓 مرحباً بك في UniBot API',
        'endpoints': {
            'register': 'POST /api/register/ (وأيضاً بدون السلاش)',
            'login':    'POST /api/login/ (وأيضاً بدون السلاش)',
            'events':   'GET  /api/events/ (وأيضاً بدون السلاش)',
            'event_detail': 'GET /api/events/<slug>/',
            'search':   'POST /api/search/ (محمية)',
            'ai_general': 'POST /api/ai/general/ (محمية)',
            'profile':  'GET/PUT /api/profile/ (محمية)',
            'ai_models': 'GET /api/ai/models/ (اختياري للتشخيص)',
            'ai_health': 'GET /api/ai/health/ (تشخيص سريع)',
        },
        'status': '✅ API جاهز للعمل'
    })


# =========================
# إنشاء حساب جديد
# =========================
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    name = _clean_text(request.data.get('name'))
    email = _clean_text(request.data.get('email'))
    password = request.data.get('password')
    role = _clean_text(request.data.get('role') or 'student')

    if not all([email, password]):
        return Response({'error': 'الرجاء إدخال البريد وكلمة المرور.'},
                        status=status.HTTP_400_BAD_REQUEST)

    if CustomUser.objects.filter(email=email).exists():
        return Response({'error': 'البريد الإلكتروني مستخدم مسبقاً.'},
                        status=status.HTTP_400_BAD_REQUEST)

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


# =========================
# الذكاء الاصطناعي
# =========================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ai_general(request):
    """
    يستقبل: { "prompt": "..." }
    يرجع:   { "result": "..." }
    - يرد بسرعة على التحيات.
    - يستدعي ask_gemini() (التي تقرأ أحدث PDF/نص من قاعدة المعرفة).
    - يرجع 200 حتى لو رد نصّياً برسالة خطأ ودّية، عشان الواجهة تعرضها.
    """
    user = request.user
    user_prompt = _clean_text(request.data.get('prompt'))

    if not user_prompt:
        return Response({'error': 'يرجى إدخال السؤال.'}, status=status.HTTP_400_BAD_REQUEST)

    # ردّ سريع للتحيات (توسيع الصيغ الشائعة)
    greetings = [
        "السلام عليكم", "وعليكم السلام", "مرحبا", "مرحبا!", "مرحبا،", "هلا",
        "يا هلا", "أهلاً", "اهلا", "صباح الخير", "مساء الخير"
    ]
    if any(g in user_prompt for g in greetings):
        name = user.name or "الطالب"
        return Response({'result': f"وعليكم السلام {name}! 👋 كيف أقدر أساعدك اليوم؟"})

    # استدعاء Gemini عبر خدمة ai_service (مع تغليف آمن)
    try:
        answer = (ask_gemini(user_prompt) or "").strip()
    except Exception as e:
        answer = f"⚠️ حدث خطأ في خدمة الذكاء: {e}"

    return Response({'result': answer}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def ai_models(request):
    """
    نقطة تشخيصية: تُرجع نسخة google-generativeai وقائمة النماذج
    التي تدعم generateContent (تفيدنا إذا صار لخبطة إصدارات).
    """
    try:
        ver = getattr(genai, "__version__", "unknown")
        names = []
        for m in genai.list_models():
            if getattr(m, "supported_generation_methods", []) and "generateContent" in m.supported_generation_methods:
                names.append(m.name)
        return Response({"genai_version": ver, "models": names})
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['GET'])
@permission_classes([AllowAny])
def ai_health(_request):
    """تشخيص سريع للـ API بدون مصادقة."""
    return Response({"ok": True, "service": "unibot-ai", "ts": timezone.now().isoformat()})


# =========================
# الملف الشخصي
# =========================
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    user = request.user

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    # PUT
    data = request.data
    user.name = _clean_text(data.get('name')) or user.name
    user.role = _clean_text(data.get('role')) or user.role
    user.save()
    serializer = UserSerializer(user)
    return Response({
        'message': '✅ تم تحديث الملف الشخصي بنجاح',
        'user': serializer.data
    })
