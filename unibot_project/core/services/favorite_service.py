# خدمة المفضلة الكاملة (Full FavoriteService - optional)
from ..models import Favorite, FAQ

class FavoriteService:
    @staticmethod
    def toggle_favorite(user_id, faq_id):
        # تبديل المفضلة (toggle_favorite(user_id, faq_id) - returns True if added, False if removed)
        try:
            faq = FAQ.objects.get(id=faq_id)  # التحقق من السؤال (Verify FAQ)
            favorite, created = Favorite.objects.get_or_create(user_id=user_id, faq=faq)
            if not created:
                favorite.delete()  # إزالة إذا موجود (Remove if exists)
                return False  # تم الإزالة (Removed)
            return True  # تم الإضافة (Added)
        except FAQ.DoesNotExist:
            raise ValueError("سؤال غير موجود")

    @staticmethod
    def list_favorites(user_id):
        # قائمة المفضلة لمستخدم (list_favorites(user_id))
        favorites = Favorite.objects.filter(user_id=user_id).select_related('faq')
        return list(favorites.values('id', 'faq__id', 'faq__question', 'created_at'))
