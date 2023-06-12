# Generated by Django 3.2.15 on 2023-01-07 13:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_shop', '0010_rename_productreview_review'),
        ('app_orders', '0009_alter_order_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='orders', to='app_orders.delivery', verbose_name='способ доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.CharField(choices=[('card', 'Онлайн картой'), ('account', 'Онлайн со случайного чужого счёта')], default='card', max_length=20, verbose_name='способ оплаты'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='order_items', to='app_shop.product', verbose_name='товар'),
        ),
    ]