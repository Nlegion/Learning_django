# Generated by Django 2.2 on 2021-02-03 19:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='имя категории')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
                ('short_desc', models.CharField(blank=True, max_length=200, verbose_name='краткое описание')),
            ],
            options={
                'verbose_name': 'категория продукта',
                'verbose_name_plural': 'категории продуктов',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='имя')),
                ('image', models.ImageField(blank=True, upload_to='products_images')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
                ('short_desc', models.CharField(blank=True, max_length=200, verbose_name='краткое описание')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='цена')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='количество на складе')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.ProductCategory')),
            ],
            options={
                'verbose_name': 'продукт',
                'verbose_name_plural': 'продукты',
                'ordering': ['name'],
            },
        ),
    ]