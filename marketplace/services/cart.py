from django.conf import settings


class Cart(object):
    def __init__(self, request):
        """ Инициализация корзины """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

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

    def clear(self):
        """ Удаление корзины из сессии """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
