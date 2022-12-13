from django.db.models import QuerySet
from app_shop.models import Product, Review
from app_users.models import CustomUser


class ProductReview:
    """ Отзывы на товар """

    def __init__(self, product: Product):
        self._product = product

    def add_review(self, user: CustomUser, text: str):
        """ Добавляет отзыв к товару """
        review = Review.objects.filter(product=self._product, user=user)
        if not review:
            Review.objects.create(product=self._product, user=user, text=text)
            return True
        return False

    def get_reviews(self) -> QuerySet:
        """ Возвращает список отзывов к товару """
        return Review.objects.filter(product=self._product).\
            select_related('user').\
            only('text', 'created_at', 'user__avatar', 'user__first_name')

    def get_reviews_amount(self) -> int:
        """ Возвращает количество отзывов для товара """
        return self.get_reviews().count()
