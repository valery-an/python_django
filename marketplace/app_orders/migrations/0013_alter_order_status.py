# Generated by Django 3.2.15 on 2023-01-16 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0012_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('wait', 'Ожидается оплата'), ('paid', 'Оплачен'), ('npaid', 'Не оплачен')], default='npaid', max_length=20, verbose_name='статус оплаты'),
        ),
    ]
