# Generated by Django 3.2.15 on 2023-01-16 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_orders', '0011_auto_20230113_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('wait', 'Ожидается оплата'), ('paid', 'Оплачен'), ('npaid', 'Не оплачен')], default='new', max_length=20, verbose_name='статус оплаты'),
        ),
    ]
