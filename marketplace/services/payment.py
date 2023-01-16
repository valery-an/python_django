from app_orders.tasks import pay_order_task


def pay_order(order_id, account):
    pay_order_task.delay(order_id, account)
