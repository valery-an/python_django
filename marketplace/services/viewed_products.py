from django.db.models import QuerySet
from django.utils import timezone
from app_users.models import CustomUser
from app_shop.models import Product, ProductViewed


class History:
    """ Просмотренные товары пользователя """

    def __init__(self, user: CustomUser):
        self.user = user

    def __len__(self) -> int:
        """ Количество просмотренных товаров пользователя """
        return ProductViewed.objects.filter(user=self.user).count()

    def add_product(self, product: Product):
        """ Добавляет товар в список просмотренных или обновляет дату просмотра, если он там уже есть """
        if self.user.is_authenticated:
            ProductViewed.objects.update_or_create(
                user=self.user,
                product=product,
                defaults={'viewed_at': timezone.now}
            )

    def delete_products(self):
        """ Удаляет товары из истории просмотров """
        if self.user.is_authenticated:
            while len(self) > 8:
                ProductViewed.objects.filter(user=self.user).last().delete()

    def get_products(self, products_number=8) -> QuerySet:
        """ Возвращает последние просмотренные товары """
        products = ProductViewed.objects.filter(user=self.user).select_related('product').filter(product__amount__gte=1)
        return products[:products_number]
