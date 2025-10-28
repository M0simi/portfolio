# خدمة الأسئلة الشائعة الكاملة (Full FaqService)
from django.db.models import Q  # للبحث المنطقي (For Q search)
from ..models import FAQ, Category

class FaqService:
    @staticmethod
    def list_faqs(query='', category_id=None):
        # قائمة الأسئلة مع بحث وتصفية (list_faqs(query, category_id) - returns dict list)
        faqs = FAQ.objects.all().select_related('category')  # تحميل الفئة مسبقًا للكفاءة (Prefetch category)
        if query:
            faqs = faqs.filter(Q(question__icontains=query) | Q(answer__icontains=query))  # بحث غير حساس (Case-insensitive search)
        if category_id:
            faqs = faqs.filter(category_id=category_id)  # تصفية بالفئة (Filter by category)
        return list(faqs.values('id', 'question', 'answer', 'category__name', 'created_at', 'updated_at'))  # إرجاع كـ dict (Dict for JSON)

    @staticmethod
    def get_faq(id):
        # الحصول على سؤال واحد (get_faq(id))
        try:
            return FAQ.objects.select_related('category', 'updated_by').get(id=id)  # مع روابط (With relations)
        except FAQ.DoesNotExist:
            return None

    @staticmethod
    def create_faq(data, user):
        # إنشاء سؤال جديد (create_faq(data, user))
        try:
            category = Category.objects.get(id=data['category_id'])  # الحصول على الفئة (Get category)
            faq = FAQ.objects.create(
                question=data['question'],
                answer=data['answer'],
                category=category,
                updated_by=user  # ربط بالمستخدم (Link to user)
            )
            return faq
        except Category.DoesNotExist:
            raise ValueError("فئة غير موجودة")  # خطأ في الفئة (Category error)

    @staticmethod
    def update_faq(id, data, user):
        # تحديث سؤال (update_faq(id, data, user))
        faq = FaqService.get_faq(id)  # الحصول أولاً (Get first)
        if faq:
            if 'question' in data:
                faq.question = data['question']
            if 'answer' in data:
                faq.answer = data['answer']
            if 'category_id' in data:
                faq.category = Category.objects.get(id=data['category_id'])
            faq.updated_by = user  # تحديث المستخدم (Update user)
            faq.save()
            return faq
        return None

    @staticmethod
    def delete_faq(id):
        # حذف سؤال (delete_faq(id))
        faq = FaqService.get_faq(id)
        if faq:
            faq.delete()
            return True
        return False
