# خدمة التعليقات الكاملة (Full FeedbackService)
from ..models import Feedback, FAQ

class FeedbackService:
    @staticmethod
    def submit_feedback(faq_id, helpful, comment, user):
        # إرسال تعليق (submit_feedback(faq_id, helpful, comment, user))
        try:
            faq = FAQ.objects.get(id=faq_id)  # الحصول على السؤال (Get FAQ)
            feedback = Feedback.objects.create(
                faq=faq,
                helpful=helpful,
                comment=comment or '',  # تعليق فارغ إذا None (Empty if none)
                user=user
            )
            return feedback
        except FAQ.DoesNotExist:
            raise ValueError("سؤال غير موجود")  # FAQ not found

    @staticmethod
    def list_feedback(faq_id):
        # قائمة تعليقات لسؤال (list_feedback(faq_id))
        try:
            feedbacks = Feedback.objects.filter(faq_id=faq_id).select_related('user')
            return list(feedbacks.values('id', 'user__email', 'helpful', 'comment', 'created_at'))
        except:
            return []
