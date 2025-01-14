# Generated by Django 3.2.15 on 2023-01-16 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0013_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_error',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Оплата не выполнена, на вашем счёте недостаточно средств'), (2, 'Оплата не выполнена, произошёл сбой при списании средств'), (3, 'Оплата не выполнена, проверьте корректность данных карты'), (4, 'Оплата не выполнена, т.к. вы подозреваетесь в нетолерантности'), (5, 'Что-то пошло не так. Попробуйте в другой раз.')], default=0, verbose_name='ошибка заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('wait', 'Ожидается оплата'), ('paid', 'Оплачен'), ('not_paid', 'Не оплачен')], default='not_paid', max_length=20, verbose_name='статус оплаты'),
        ),
    ]
