# Generated by Django 3.2.15 on 2022-11-22 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='icon_path',
            field=models.FilePathField(path='/static/assets/img/icons/departments/', verbose_name='символ'),
        ),
    ]
