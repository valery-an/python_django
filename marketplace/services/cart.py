from django.conf import settings
from app_shop.models import Product


class Cart(object):
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
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product
        for item in self.cart.values():
            yield item

    def __len__(self):
        """ Подсчет всех товаров в корзине """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1):
        """ Добавление товара в корзину или обновление его количества """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': quantity,
                                     'price': product.price}
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        """ Удаление товара из корзины """
        product_id = str(product.id)
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
