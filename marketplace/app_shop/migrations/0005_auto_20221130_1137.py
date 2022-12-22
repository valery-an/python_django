# Generated by Django 3.2.15 on 2022-11-30 08:37

import app_shop.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_shop', '0004_auto_20221123_1317'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.RemoveField(
            model_name='product',
            name='short_description',
        ),
        migrations.AddField(
            model_name='product',
            name='added_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='дата добавления'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='parameters',
            field=models.TextField(blank=True, max_length=100000, verbose_name='характеристики'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=100000, verbose_name='текст')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='app_shop.product', verbose_name='товар')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'отзыв',
                'verbose_name_plural': 'отзывы',
                'db_table': 'reviews',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='goods/no_image.png', upload_to=app_shop.models.get_upload_path, verbose_name='изображение')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='app_shop.product', verbose_name='товар')),
            ],
            options={
                'verbose_name': 'изображение товара',
                'verbose_name_plural': 'изображения товара',
                'db_table': 'product_images',
            },
        ),
    ]
