# خدمة البحث الكاملة (Full SearchService - ORM بسيط، جاهز لـ Rasa/Vector)
from django.db.models import Q
from ..models import FAQ

class SearchService:
    @staticmethod
    def search(query, top_k=5):
        # بحث في الأسئلة (search(query, top_k) - بسيط الآن، Rasa لاحقًا)
        faqs = FAQ.objects.filter(Q(question__icontains=query) | Q(answer__icontains=query)).select_related('category')[:top_k]
        return list(faqs.values('id', 'question', 'answer', 'category__name'))  # نتائج كـ dict

    @staticmethod
    def index_faq(faq):
        # فهرسة السؤال (index_faq(faq) - حفظ في DB، لاحقًا Vector Store أو Rasa)
        if isinstance(faq, dict):  # إذا data، أنشئ (If dict, create)
            from .faq_service import FaqService
            # افتراضيًا، FaqService.create_faq(faq, None) - لكن في MVP، مجرد حفظ
            pass
        else:
            faq.save()  # حفظ النموذج (Save model)
        # Future: e.g., OpenAI embedding or Rasa train
        # مثال: rasa_client.index(faq.question, faq.answer)
