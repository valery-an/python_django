from random import choice
from time import sleep
from celery import shared_task
from django.shortcuts import get_object_or_404


@shared_task
def pay_order_task(order_id, account):
    sleep(10)
    from .models import Order
    order = get_object_or_404(Order, id=order_id)
    if account % 2 == 0 and account % 10 != 0:
        order.status = 'paid'
        order.payment_error = 0
    else:
        order.status = 'not_paid'
        order.payment_error = choice(Order.ERROR_CHOICES)[0]
    order.save(update_fields=['status', 'payment_error'])
