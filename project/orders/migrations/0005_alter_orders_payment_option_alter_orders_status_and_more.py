# Generated by Django 4.1.5 on 2023-02-07 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_orders_payment_option'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='payment_option',
            field=models.CharField(blank=True, choices=[('Razorpay', 'Razorpay'), ('cash On delivery', 'cash On delivery')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='status',
            field=models.CharField(default='Confirmed', max_length=100),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
