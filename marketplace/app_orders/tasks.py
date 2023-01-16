from random import choice
from time import sleep
from celery import shared_task
from django.shortcuts import get_object_or_404
from app_orders.models import Order


@shared_task
def pay_order_task(order_id, account):
    sleep(10)
    order = get_object_or_404(Order, id=order_id)
    if account % 2 != 0 or str(account)[-1] == '0' or len(account) != 8:
        order.status = 'paid'
        order.payment_error = 0
    else:
        order.status = 'not_paid'
        order.payment_error = choice(Order.ERROR_CHOICES)[0]
    order.save(update_fields=['status', 'payment_error'])
