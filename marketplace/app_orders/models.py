from django.db import models
from app_users.models import CustomUser, Address
from app_shop.models import Product


class Delivery(models.Model):
    """ Модель доставки """
    type = models.CharField(max_length=100, verbose_name='название')
    price = models.PositiveIntegerField(verbose_name='цена')
    min_order_cost = models.PositiveIntegerField(default=0, verbose_name='мин. стоимость заказа')

    class Meta:
        db_table = 'delivery'
        verbose_name = 'доставка'
        verbose_name_plural = 'доставки'

    def __str__(self):
        return self.type


class Order(models.Model):
    """ Модель заказа """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='пользователь')
    address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name='адрес')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    cost = models.PositiveIntegerField(default=0, verbose_name='стоимость')
    is_paid = models.BooleanField(default=False, verbose_name='оплачено')
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, verbose_name='способ доставки')
    comment = models.TextField(max_length=5000, verbose_name='комментарий')

    class Meta:
        db_table = 'orders'
        default_related_name = 'orders'
        ordering = ['-created_at']
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Заказ {self.id}. Пользователь: {self.user}.'

    def get_delivery_cost(self):
        """ Возвращает стоимость доставки """
        if self.delivery.min_order_cost == 0 or self.cost < self.delivery.min_order_cost:
            return self.delivery.price
        return 0

    def get_total_cost(self):
        """ Возвращает стоимость заказа с доставкой """
        result = self.cost + self.get_delivery_cost()
        return result


class OrderItem(models.Model):
    """ Модель строки заказа """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='заказ', related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name='товар', related_name='order_items')
    quantity = models.PositiveIntegerField(default=1, verbose_name='количество')

    class Meta:
        db_table = 'order_items'
        verbose_name = 'строка заказа'
        verbose_name_plural = 'строки заказов'

    def __str__(self):
        return f'Строка заказа {self.order.id}'

    def get_price(self):
        """ Возвращает стоимость строки заказа """
        result = self.product.price * self.quantity
        return result
