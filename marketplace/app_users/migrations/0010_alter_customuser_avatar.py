# Generated by Django 3.2.15 on 2022-11-22 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0009_alter_customuser_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(default='avatars/no_image.jpg', upload_to='avatars/', verbose_name='фотография профиля'),
        ),
    ]
