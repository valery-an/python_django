# Generated by Django 3.2.15 on 2022-11-13 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0004_alter_customuser_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='second_name',
        ),
    ]
