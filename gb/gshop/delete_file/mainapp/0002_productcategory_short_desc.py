# Generated by Django 2.2 on 2021-01-30 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='short_desc',
            field=models.CharField(blank=True, max_length=200, verbose_name='краткое описание'),
        ),
    ]
