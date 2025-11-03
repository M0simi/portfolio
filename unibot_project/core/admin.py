# تسجيل النماذج الكامل في لوحة الإدارة (Full models registration in admin - fixed with explicit fieldsets)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # للمستخدم المخصص (Custom user admin)
from django.contrib.auth.forms import UserCreationForm, UserChangeForm  # نماذج الإدارة (Admin forms)
from django.utils.html import format_html
from .models import CustomUser, Category, FAQ, Event, Feedback, Favorite
from .models import KnowledgeBase

# نموذج الإنشاء المخصص للمستخدم (Custom User Creation Form - no duplicates)
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'name', 'role', 'password1', 'password2')  # حقول الإضافة بدون تكرار (Add fields - no duplicates)

# نموذج التعديل المخصص (Custom User Change Form - no duplicates)
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('email', 'name', 'role', 'is_active', 'is_staff', 'is_superuser', 'date_joined')  # حقول التعديل بدون تكرار (Change fields)

# تسجيل CustomUser مع نماذج مخصصة (Register CustomUser with explicit fieldsets - no duplicates)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm  # نموذج الإضافة (Custom add form)
    form = CustomUserChangeForm  # نموذج التعديل (Custom change form)
    list_display = ['email', 'name', 'role', 'created_at']  # عرض البريد، الاسم، الدور، التاريخ (Display fields)
    list_filter = ['role', 'created_at', 'is_staff', 'is_superuser']  # فلاتر (Filters)
    search_fields = ['email', 'name']  # بحث (Search)
    ordering = ['email']  # ترتيب حسب البريد (Order by email)
    
    # حقول الإضافة البسيطة (Add fieldsets - explicit, no username/duplicates)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'role', 'password1', 'password2'),  # email أولاً، بدون تكرار (Email first, no duplicates)
        }),
    )
    
    # حقول التعديل اليدوي البسيط (Fieldsets - explicit tuple, no deepcopy/duplicates - FIX)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),  # بيانات أساسية (Personal info - email & password)
        ('بيانات شخصية', {'fields': ('name', 'role', 'date_joined')}),  # معلومات شخصية (Personal - name, role, date)
        ('صلاحيات', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),  # Permissions (Permissions)
        ('تواريخ مهمة', {'fields': ('last_login',)}),  # Important dates (Dates)
    )
    
    # فلاتر أفقية للـ UI (Horizontal filters for UI)
    filter_horizontal = ('groups', 'user_permissions')  # تحسين عرض الصلاحيات (Improve permissions display)

admin.site.register(CustomUser, CustomUserAdmin)

# باقي الإدارات دون تغيير (Rest unchanged)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']  # عرض الاسم والتاريخ
    search_fields = ['name']  # بحث في الاسم
    ordering = ['name']  # ترتيب حسب الاسم

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'updated_by', 'updated_at']  # عرض السؤال، الفئة، المحدث، التاريخ
    list_filter = ['category', 'updated_at']  # فلاتر
    search_fields = ['question', 'answer']  # بحث في السؤال والإجابة
    raw_id_fields = ['category', 'updated_by']  # للروابط الكبيرة (Large relations)
    ordering = ['-updated_at']  # ترتيب أحدث أولاً

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    # نعرض الـ slug والصورة المصغّرة
    list_display = ['title', 'start_date', 'location', 'slug', 'image_preview']  # عرض العنوان، التاريخ، الموقع، السلاج، والصورة
    list_filter = ['start_date']  # فلاتر زمنية (نكتفي ببداية الحدث)
    date_hierarchy = 'start_date'  # تصفح حسب التاريخ
    search_fields = ['title', 'location', 'description']  # بحث شامل
    ordering = ['start_date']  # ترتيب حسب التاريخ
    prepopulated_fields = {"slug": ("title",)}  # تعبئة slug مبدئيًا من العنوان

    # تنظيم الحقول داخل صفحة التعديل/الإضافة
    fields = (
        ('title', 'slug'),
        ('start_date', 'end_date'),
        'location',
        'description',
        'image',
        'image_preview',
    )
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if getattr(obj, 'image', None):
            try:
                return format_html('<img src="{}" style="max-height:80px; border-radius:6px;" />', obj.image.url)
            except Exception:
                return '-'
        return '-'
    image_preview.short_description = 'معاينة الصورة'  # اسم العمود في لست ديسبلاي

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['faq', 'user', 'helpful', 'created_at']  # عرض السؤال، المستخدم، المفيد، التاريخ
    list_filter = ['helpful', 'created_at']  # فلاتر
    raw_id_fields = ['faq', 'user']  # روابط
    ordering = ['-created_at']  # ترتيب أحدث أولاً

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'faq', 'created_at']  # عرض المستخدم، السؤال، التاريخ
    list_filter = ['created_at']  # فلاتر
    raw_id_fields = ['user', 'faq']  # روابط
    ordering = ['-created_at']  # ترتيب أحدث أولاً

@admin.register(KnowledgeBase)
class KnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')
    search_fields = ('title',)
