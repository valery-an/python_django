from django.conf import settings
from django.shortcuts import get_object_or_404
from app_shop.models import Product


class Cart:
    def __init__(self, request):
        """ Инициализация корзины """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """ Перебор элементов в корзине и получение товаров из базы данных """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids).only('name')
        for product in products:
            self.cart[str(product.id)]['product'] = product
        for item in self.cart.values():
            yield item

    def __len__(self):
        """ Количество всех товаров в корзине """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product_id: int, quantity: int = 1):
        """ Добавление товара в корзину или обновление его количества """
        product_price = get_object_or_404(Product, id=product_id).price
        product_amount = get_object_or_404(Product, id=product_id).amount
        product_id = str(product_id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': quantity,
                                     'price': product_price}
        else:
            self.cart[product_id]['quantity'] += quantity
            if self.cart[product_id]['quantity'] > product_amount:
                self.cart[product_id]['quantity'] = product_amount
            if self.cart[product_id]['quantity'] == 0:
                self.cart[product_id]['quantity'] = 1
        self.save()

    def remove(self, product_id: int):
        """ Удаление товара из корзины """
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        """ Сохранение корзины """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def get_total_price(self):
        """ Подсчет итоговой стоимости товаров в корзине """
        total_price = sum(item['price'] * item['quantity'] for item in self.cart.values())
        return total_price

    def clear(self):
        """ Удаление корзины из сессии """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
