# محولات البيانات الكاملة للـ API (Full serializers for all models)
from rest_framework import serializers
from .models import CustomUser, Category, FAQ, Event, Feedback, Favorite
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    # محول المستخدم (User serializer)
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'role', 'created_at']  # حقول الإخراج (Output fields)
        read_only_fields = ['id', 'created_at']  # غير قابلة للتعديل (Read-only)

class CategorySerializer(serializers.ModelSerializer):
    # محول الفئة (Category serializer)
    class Meta:
        model = Category
        fields = '__all__'  # جميع الحقول (All fields)

class FAQSerializer(serializers.ModelSerializer):
    # محول الـ FAQ مع روابط (FAQ serializer with relations)
    category = CategorySerializer(read_only=True)  # عرض الفئة (Category details)
    updated_by = UserSerializer(read_only=True)  # عرض المحدث (Updater details)
    
    class Meta:
        model = FAQ
        fields = '__all__'  # جميع
        read_only_fields = ['id', 'created_at', 'updated_at']  # ID وتواريخ غير قابلة للتعديل

class EventSerializer(serializers.ModelSerializer):
    # محول الحدث مع رابط صورة كامل (Event serializer with absolute image URL)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Event
        # إظهار الحقول المتفق عليها فقط (بدون image الخام)
        fields = [
            'id', 'title', 'slug',
            'start_date', 'end_date',
            'location', 'description',
            'image_url'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if getattr(obj, 'image', None):
            url = obj.image.url
            return request.build_absolute_uri(url) if request else url
        return None

class FeedbackSerializer(serializers.ModelSerializer):
    # محول التعليق (Feedback serializer)
    faq = FAQSerializer(read_only=True)  # عرض السؤال (FAQ details)
    user = UserSerializer(read_only=True)  # عرض المستخدم (User details)
    
    class Meta:
        model = Feedback
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

class FavoriteSerializer(serializers.ModelSerializer):
    # محول المفضلة (Favorite serializer)
    faq = FAQSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Favorite
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'password', 'role']
        read_only_fields = ['id']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return CustomUser.objects.create(**validated_data)
