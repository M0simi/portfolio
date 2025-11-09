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

    status_param = (request.GET.get('status') or '').lower()
    if status_param == 'upcoming':
        qs = qs.filter(start_date__gte=now)
    elif status_param == 'past':
        qs = qs.filter(Q(end_date__lt=now) | Q(end_date__isnull=True, start_date__lt=now))
    # else: all

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
    query = request.data.get('query', '').strip()
    faqs = FAQ.objects.filter(question__icontains=query)[:5] if query else []
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
            'event_detail': 'GET /api/events/<slug>/',
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


# ✅ بوت الذكاء (Gemini)
@api_view(['GET'])
@permission_classes([AllowAny])
def ai_models(request):
    try:
        ver = getattr(genai, "__version__", "unknown")
        names = []
        for m in genai.list_models():
            if getattr(m, "supported_generation_methods", []) and "generateContent" in m.supported_generation_methods:
                names.append(m.name)
        return Response({"genai_version": ver, "models": names})
    except Exception as e:
        return Response({"error": str(e)}, status=500)


# ✅ الملف الشخصي
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    user = request.user

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    # PUT
    data = request.data
    user.name = data.get('name', user.name)
    user.role = data.get('role', user.role)
    user.save()
    serializer = UserSerializer(user)
    return Response({
        'message': '✅ تم تحديث الملف الشخصي بنجاح',
        'user': serializer.data
    })

