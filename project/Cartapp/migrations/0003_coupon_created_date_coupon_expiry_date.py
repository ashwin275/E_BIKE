# Generated by Django 4.1.5 on 2023-02-09 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cartapp', '0002_alter_cartitem_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='created_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='coupon',
            name='expiry_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
