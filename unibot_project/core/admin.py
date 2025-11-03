from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # للمستخدم المخصص (Custom user admin)
from django.contrib.auth.forms import UserCreationForm, UserChangeForm  # نماذج الإدارة (Admin forms)
from django.utils.html import format_html
from .models import CustomUser, Category, FAQ, Event, Feedback, Favorite, KnowledgeBase


# نموذج الإنشاء المخصص للمستخدم (Custom User Creation Form - no duplicates)
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'name', 'role', 'password1', 'password2')


# نموذج التعديل المخصص (Custom User Change Form - no duplicates)
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('email', 'name', 'role', 'is_active', 'is_staff', 'is_superuser', 'date_joined')


# تسجيل CustomUser مع نماذج مخصصة
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['email', 'name', 'role', 'created_at']
    list_filter = ['role', 'created_at', 'is_staff', 'is_superuser']
    search_fields = ['email', 'name']
    ordering = ['email']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'role', 'password1', 'password2'),
        }),
    )

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('بيانات شخصية', {'fields': ('name', 'role', 'date_joined')}),
        ('صلاحيات', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('تواريخ مهمة', {'fields': ('last_login',)}),
    )

    filter_horizontal = ('groups', 'user_permissions')


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['name']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'updated_by', 'updated_at']
    list_filter = ['category', 'updated_at']
    search_fields = ['question', 'answer']
    raw_id_fields = ['category', 'updated_by']
    ordering = ['-updated_at']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    # نعرض الـ slug والصورة المصغّرة
    list_display = ['title', 'start_date', 'location', 'slug', 'image_preview']
    list_filter = ['start_date']
    date_hierarchy = 'start_date'
    search_fields = ['title', 'location', 'description']
    ordering = ['start_date']
    prepopulated_fields = {"slug": ("title",)}

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
        """
        تعرض رابط مباشر للصورة + معاينة مصغّرة.
        لا تكسر الصفحة لو الملف مفقود (مثلاً بعد إعادة نشر على Render).
        """
        img = getattr(obj, 'image', None)
        if img and getattr(img, 'url', None):
            url = img.url
            return format_html(
                "<div style='display:flex;flex-direction:column;gap:6px'>"
                "<a href='{0}' target='_blank' style='word-break:break-all'>{0}</a>"
                "<img src='{0}' style='max-height:120px;border-radius:6px;object-fit:cover'/>"
                "</div>",
                url
            )
        return "—"
    image_preview.short_description = 'معاينة الصورة'


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['faq', 'user', 'helpful', 'created_at']
    list_filter = ['helpful', 'created_at']
    raw_id_fields = ['faq', 'user']
    ordering = ['-created_at']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'faq', 'created_at']
    list_filter = ['created_at']
    raw_id_fields = ['user', 'faq']
    ordering = ['-created_at']


@admin.register(KnowledgeBase)
class KnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')
    search_fields = ('title',)
