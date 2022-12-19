from django.shortcuts import render, redirect
from services.cart import Cart


def add_product_to_cart(request, pk):
    """ Добавление товара в корзину """
    cart = Cart(request)
    cart.add(product_id=pk)
    return redirect(request.META.get("HTTP_REFERER"))


def reduce_product_from_cart(request, pk):
    """ Уменьшение количества товара в корзине """
    cart = Cart(request)
    cart.add(product_id=pk, quantity=-1)
    return redirect(request.META.get("HTTP_REFERER"))


def remove_product_from_cart(request, pk):
    """ Удаление товара из корзины """
    cart = Cart(request)
    cart.remove(product_id=pk)
    return redirect(request.META.get("HTTP_REFERER"))


def cart_view(request):
    """ Страница корзины с возможностью оформления заказа """
    cart = Cart(request)
    return render(request, 'orders/cart.html', {'cart': cart})
