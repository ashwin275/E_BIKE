# Generated by Django 4.1.5 on 2023-02-08 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_variant_color'),
        ('orders', '0005_alter_orders_payment_option_alter_orders_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordervehicle',
            name='vehicles',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.variant'),
        ),
    ]
