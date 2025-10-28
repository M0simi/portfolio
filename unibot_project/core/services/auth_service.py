# خدمة المصادقة الكاملة (Full AuthService)
from rest_framework.authtoken.models import Token  # نموذج التوكن (Token model)
from django.contrib.auth import authenticate  # دالة المصادقة (Auth function)
from django.contrib.auth.hashers import make_password  # تشفير كلمة المرور (Password hashing)
from ..models import CustomUser  # استيراد CustomUser
import uuid

class AuthService:
    @staticmethod
    def login(email, password):
        # تسجيل الدخول: يتحقق ويعيد توكن (login(email, password) → token or None)
        user = authenticate(username=email, password=password)  # مصادقة Django (Django auth)
        if user and user.is_active:  # إذا نجح ومفعل (If valid and active)
            token, created = Token.objects.get_or_create(user=user)  # الحصول أو إنشاء توكن (Get or create token)
            return {
                'token': token.key,
                'user': {
                    'id': str(user.id),  # UUID كـ string لـ JSON
                    'name': user.name,
                    'email': user.email,
                    'role': user.role
                }
            }
        return None  # فشل (Failure)

    @staticmethod
    def generate_token(user):
        # توليد توكن جديد (generate_token(user))
        if isinstance(user, str):  # إذا email، ابحث (If string, find user)
            user = CustomUser.objects.get(email=user)
        token = Token.objects.create(user=user)  # إنشاء توكن (Create token)
        return token.key

    @staticmethod
    def verify_token(token_key):
        # التحقق من التوكن (verify_token(token))
        try:
            token = Token.objects.get(key=token_key)  # البحث عن التوكن (Get token)
            return token.user if token.user.is_active else None  # إرجاع المستخدم إذا مفعل (Return active user)
        except Token.DoesNotExist:
            return None  # غير موجود (Not found)
