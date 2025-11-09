# نماذج قاعدة البيانات الكاملة والمتكيفة مع SQLite (Full adapted models for SQLite from MongoDB - updated with fixed Manager)
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager  # استيراد BaseUserManager للمخصص (BaseUserManager for custom)
from django.utils.text import slugify  # لتوليد slug من العنوان (Generate slug from title)
import uuid  # مكتبة UUID للـ _id (UUID library for _id)
from cloudinary_storage.storage import RawMediaCloudinaryStorage

# مدير المستخدم المخصص (Custom User Manager - FIXED with self.model)
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # إنشاء مستخدم عادي (create_user - handles email instead of username)
        if not email:
            raise ValueError('يجب إدخال البريد الإلكتروني')  # Email required
        email = self.normalize_email(email)  # تنظيف البريد (Normalize email)
        extra_fields.setdefault('is_active', True)  # نشط افتراضيًا (Active by default)
        user = self.model(email=email, **extra_fields)  # إنشاء النموذج - FIXED: self.model (not Model)
        if password:
            user.set_password(password)  # تشفير كلمة المرور (Set hashed password - uses AbstractUser)
        user.save(using=self._db)  # حفظ (Save)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # إنشاء إداري (create_superuser - for createsuperuser command)
        extra_fields.setdefault('is_staff', True)  # صلاحيات إدارية (Staff permissions)
        extra_fields.setdefault('is_superuser', True)  # سوبريوزر (Superuser)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('الإداري يجب أن يكون is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('الإداري يجب أن يكون is_superuser=True.')
        return self.create_user(email, password, **extra_fields)  # استخدام create_user (Use create_user)

class CustomUser(AbstractUser):
    # جدول users - ممتد من Django User ليتناسب مع التصميم (Users table - extended for schema)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # _id: UUID (UUID primary key)
    email = models.EmailField(unique=True)  # email: string (unique) - مطلوب (Unique email)
    name = models.CharField(max_length=100, blank=True)  # name: string (optional)
    role = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('student', 'Student')], default='student')  # role: admin|student
    # لا تضع password هنا؛ AbstractUser يديره (No password field; AbstractUser handles it)
    created_at = models.DateTimeField(auto_now_add=True)  # created_at: ISODate (Auto creation)
    updated_at = models.DateTimeField(auto_now=True)  # updated_at: ISODate (Auto update)
    
    # إعدادات المصادقة (Authentication settings)
    objects = CustomUserManager()  # استخدام المدير المخصص (Use custom manager)
    
    # إزالة username الافتراضي، استخدم email (Remove default username)
    username = None
    USERNAME_FIELD = 'email'  # حقل المصادقة الرئيسي (Primary auth field)
    REQUIRED_FIELDS = []  # لا حقول إضافية مطلوبة (No additional required - name is optional)
    
    def __str__(self):
        return self.email  # تمثيل كنص (String representation)
    
    class Meta:
        verbose_name = 'مستخدم'  # اسم في الإدارة (Admin name)
        verbose_name_plural = 'مستخدمون'  # جمع (Plural)

# باقي النماذج دون تغيير (Rest of models unchanged)
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # _id: UUID
    name = models.CharField(max_length=100)  # name: string
    
    created_at = models.DateTimeField(auto_now_add=True)  # created_at
    updated_at = models.DateTimeField(auto_now=True)  # updated_at
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'فئة'
        verbose_name_plural = 'فئات'
        ordering = ['name']

class FAQ(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # _id: UUID
    question = models.TextField()  # question: text
    answer = models.TextField()    # answer: text
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='faqs')  # category_id -> Category (ForeignKey)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_faqs')  # updated_by -> User
    created_at = models.DateTimeField(auto_now_add=True)  # created_at
    updated_at = models.DateTimeField(auto_now=True)  # updated_at
    
    def __str__(self):
        return self.question[:50] + '...'  # عرض قصير (Short preview)
    
    class Meta:
        verbose_name = 'سؤال شائع'
        verbose_name_plural = 'أسئلة شائعة'
        ordering = ['-updated_at']  # ترتيب أحدث أولاً (Latest first)

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # _id: UUID
    title = models.CharField(max_length=200)  # title: string
    slug = models.SlugField(max_length=220, unique=True, db_index=True, blank=True)  # جديد: رابط نظيف (unique, indexed)
    start_date = models.DateTimeField()  # start_date: ISODate
    end_date = models.DateTimeField(null=True, blank=True)  # end_date: ISODate (optional)
    location = models.CharField(max_length=100, blank=True)  # location: string
    description = models.TextField(blank=True)  # description: string
    image = models.ImageField(upload_to='events/', null=True, blank=True)  # جديد: صورة الحدث (optional)
    created_at = models.DateTimeField(auto_now_add=True)  # created_at
    updated_at = models.DateTimeField(auto_now=True)  # updated_at

    def save(self, *args, **kwargs):
        # توليد slug تلقائيًا من العنوان مع ضمان التفرد (Auto-generate unique slug from title)
        if not self.slug:
            base = slugify(self.title)[:200]
            candidate = base
            i = 1
            while Event.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                i += 1
                candidate = f"{base}-{i}"
            self.slug = candidate
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'حدث'
        verbose_name_plural = 'أحداث'
        ordering = ['start_date']

class Feedback(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # _id: UUID
    faq = models.ForeignKey(FAQ, on_delete=models.CASCADE, related_name='feedbacks')  # faq_id -> FAQ
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedbacks')  # user_id -> User
    helpful = models.BooleanField(default=True)  # helpful: boolean
    comment = models.TextField(blank=True)  # comment: string
    created_at = models.DateTimeField(auto_now_add=True)  # created_at
    
    def __str__(self):
        return f"تعليق على {self.faq.question[:20]}"  # Short description
    
    class Meta:
        verbose_name = 'تعليق'
        verbose_name_plural = 'تعليقات'
        ordering = ['-created_at']

class Favorite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # _id: UUID
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorites')  # user_id -> User
    faq = models.ForeignKey(FAQ, on_delete=models.CASCADE, related_name='favorites')  # faq_id -> FAQ
    created_at = models.DateTimeField(auto_now_add=True)  # created_at
    
    class Meta:
        unique_together = ('user', 'faq')  # منع التكرار للمستخدم والسؤال (Unique user-FAQ pair)
        verbose_name = 'مفضلة'
        verbose_name_plural = 'المفضلات'
    
    def __str__(self):
        return f"{self.user.email} - {self.faq.question[:20]}"


from django.db import models
from cloudinary_storage.storage import RawMediaCloudinaryStorage  # سطر مهم

class KnowledgeBase(models.Model):
    title = models.CharField(max_length=255)
  

    file = models.FileField(
        upload_to='knowledge/',
        storage=RawMediaCloudinaryStorage(),   
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(auto_now=True)


