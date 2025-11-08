from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.html import format_html
from .models import CustomUser, Category, FAQ, Event, Feedback, Favorite, KnowledgeBase


# ==========================
# تخصيص عناوين الأدمن
# ==========================
admin.site.site_header = "لوحة إدارة UniBot"
admin.site.site_title = "UniBot Admin"
admin.site.index_title = "إدارة الموقع"


# ==========================
# نماذج المستخدم المخصص
# ==========================
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'name', 'role', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('email', 'name', 'role', 'is_active', 'is_staff', 'is_superuser', 'date_joined')


# ==========================
# إدارة المستخدم المخصص
# ==========================
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['email', 'name', 'role', 'is_staff', 'created_at']
    list_filter = ['role', 'is_staff', 'is_superuser', 'is_active', 'created_at']
    search_fields = ['email', 'name']
    ordering = ['-created_at']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'role', 'password1', 'password2'),
        }),
    )

    fieldsets = (
        ('🔐 معلومات الدخول', {'fields': ('email', 'password')}),
        ('👤 البيانات الشخصية', {'fields': ('name', 'role', 'date_joined')}),
        ('⚙️ الصلاحيات', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('📅 التواريخ', {'fields': ('last_login',)}),
    )

    filter_horizontal = ('groups', 'user_permissions')


# ==========================
# إدارة التصنيفات
# ==========================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['name']
    list_per_page = 20


# ==========================
# إدارة الأسئلة الشائعة
# ==========================
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'updated_by', 'updated_at']
    list_filter = ['category', 'updated_at']
    search_fields = ['question', 'answer']
    raw_id_fields = ['category', 'updated_by']
    ordering = ['-updated_at']
    list_per_page = 20
    
    fieldsets = (
        ('📝 السؤال والجواب', {
            'fields': ('question', 'answer', 'category')
        }),
        ('👤 معلومات التحديث', {
            'fields': ('updated_by', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('updated_at',)


# ==========================
# إدارة الفعاليات
# ==========================
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'location', 'slug', 'image_preview']
    list_filter = ['start_date']
    date_hierarchy = 'start_date'
    search_fields = ['title', 'location', 'description']
    ordering = ['-start_date']
    prepopulated_fields = {"slug": ("title",)}
    list_per_page = 20

    fieldsets = (
        ('📌 معلومات الفعالية', {
            'fields': (('title', 'slug'), 'description')
        }),
        ('📅 التواريخ والموقع', {
            'fields': (('start_date', 'end_date'), 'location')
        }),
        ('🖼️ الصورة', {
            'fields': ('image', 'image_preview')
        }),
    )
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        """عرض معاينة الصورة مع رابط مباشر"""
        img = getattr(obj, 'image', None)
        if img and getattr(img, 'url', None):
            url = img.url
            return format_html(
                "<div style='display:flex;flex-direction:column;gap:8px'>"
                "<a href='{0}' target='_blank' style='color:#3b82f6;word-break:break-all'>"
                "🔗 فتح الصورة في تبويب جديد"
                "</a>"
                "<img src='{0}' style='max-height:150px;border-radius:8px;object-fit:cover;box-shadow:0 2px 8px rgba(0,0,0,0.1)'/>"
                "</div>",
                url
            )
        return format_html("<span style='color:#94a3b8'>— لا توجد صورة —</span>")
    
    image_preview.short_description = '🖼️ معاينة الصورة'


# ==========================
# إدارة التقييمات
# ==========================
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['faq', 'user', 'helpful_status', 'created_at']
    list_filter = ['helpful', 'created_at']
    raw_id_fields = ['faq', 'user']
    ordering = ['-created_at']
    list_per_page = 20
    
    def helpful_status(self, obj):
        """عرض الحالة بشكل أجمل"""
        if obj.helpful:
            return format_html('<span style="color:green;font-weight:bold">✅ مفيد</span>')
        return format_html('<span style="color:red;font-weight:bold">❌ غير مفيد</span>')
    
    helpful_status.short_description = 'التقييم'


# ==========================
# إدارة المفضلة
# ==========================
@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'faq', 'created_at']
    list_filter = ['created_at']
    raw_id_fields = ['user', 'faq']
    ordering = ['-created_at']
    list_per_page = 20


# ==========================
# إدارة قاعدة المعرفة
# ==========================
@admin.register(KnowledgeBase)
class KnowledgeBaseAdmin(admin.ModelAdmin):
    # اعرض العنوان والملف وتاريخ التحديث
    list_display = ("id", "title", "file", "updated_at")
    search_fields = ("title",)  
    ordering = ["-updated_at"]
    list_per_page = 20

    fieldsets = (
        ("📚 المحتوى", {
            "fields": ("title", "file")  
        }),
        ("📅 التواريخ", {
            "fields": ("updated_at",),
            "classes": ("collapse",),
        }),
    )

    readonly_fields = ("updated_at",)


