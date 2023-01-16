from django.contrib.auth import authenticate, login
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from app_orders.forms import OrderForm
from app_orders.models import OrderItem, Order
from app_shop.models import Product
from app_users.forms import RegisterForm, ProfileForm

from services.cart import Cart
from services.payment import pay_order


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
    """ Страница корзины """
    cart = Cart(request)
    return render(request, 'orders/cart.html', {'cart': cart})


def create_order_view(request):
    """ Страница оформления заказа """
    cart = Cart(request)
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
        else:
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                email = form.cleaned_data.get('email')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(email=email, password=raw_password)
                login(request, user)
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.user = request.user
            order.cost = cart.get_total_price()
            products = []
            order_items = []
            for item in cart:
                product = item['product']
                quantity = item['quantity']
                order_items.append(OrderItem(order=order, product=product, quantity=quantity))
                products.append(product)
                product.amount -= quantity
            with transaction.atomic():
                order.save()
                OrderItem.objects.bulk_create(order_items)
                Product.objects.bulk_update(products, ['amount'])
                cart.clear()
            return redirect('payment', pk=order.id)
    if request.user.is_authenticated:
        form = ProfileForm(instance=request.user)
    else:
        form = RegisterForm()
    order_form = OrderForm()
    return render(request, 'orders/order.html', {'cart': cart, 'form': form, 'order_form': order_form})


def payment_view(request, pk):
    """ Оплата заказа """
    order = get_object_or_404(Order, id=pk)
    if request.method == 'POST':
        account = request.POST.get('numero1')
        order.status = 'wait'
        order.payment_error = 0
        order.save(update_fields=['status', 'payment_error'])
        pay_order(pk, account)
        return redirect('order_history')
    return render(request, 'orders/payment.html', {'order': order})


class OrderListView(ListView):
    template_name = 'orders/order_history.html'
    context_object_name = 'orders_list'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/one_order.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.object.user
        order_items = OrderItem.objects.filter(order=self.object).select_related('product')
        context['order_items'] = order_items
        return context
