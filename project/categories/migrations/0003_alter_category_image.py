# Generated by Django 4.1.5 on 2023-01-17 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(default='', null=True, upload_to='category'),
        ),
    ]
