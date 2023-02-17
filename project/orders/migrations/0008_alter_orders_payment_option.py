# Generated by Django 4.1.5 on 2023-02-17 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_orders_booking_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='payment_option',
            field=models.CharField(blank=True, choices=[('razorpay', 'razorpay'), ('COD', 'COD')], max_length=30, null=True),
        ),
    ]
