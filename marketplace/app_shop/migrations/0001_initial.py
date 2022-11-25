# Generated by Django 3.2.15 on 2022-11-06 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='название')),
                ('icon_path', models.FilePathField(path='static/assets/img/icons/departments/', verbose_name='символ')),
                ('sorting_index', models.PositiveSmallIntegerField(unique=True, verbose_name='индекс сортировки')),
                ('is_active', models.BooleanField(default=True, verbose_name='активно')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
                'db_table': 'product_categories',
                'ordering': ['sorting_index'],
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='название бренда')),
                ('about', models.TextField(blank=True, max_length=10000, verbose_name='о компании')),
                ('logo', models.ImageField(blank=True, upload_to='logos/', verbose_name='логотип')),
            ],
            options={
                'verbose_name': 'магазин',
                'verbose_name_plural': 'магазины',
                'db_table': 'shops',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='название')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='app_shop.category', verbose_name='категория')),
            ],
            options={
                'verbose_name': 'подкатегория',
                'verbose_name_plural': 'подкатегории',
                'db_table': 'product_subcategories',
                'ordering': ['category'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='название')),
                ('description', models.TextField(blank=True, max_length=100000, verbose_name='описание')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='цена')),
                ('image', models.ImageField(default='goods/no_image.png', upload_to='goods/', verbose_name='изображение')),
                ('amount', models.PositiveIntegerField(default=0, verbose_name='количество')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='app_shop.category', verbose_name='категория')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='app_shop.shop', verbose_name='бренд')),
                ('subcategory', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='app_shop.subcategory', verbose_name='подкатегория')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'товары',
                'db_table': 'products',
                'ordering': ['name'],
            },
        ),
    ]