# Generated by Django 4.1.5 on 2023-02-22 07:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_orders_total_units'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orders',
            old_name='total_units',
            new_name='no_of_items',
        ),
    ]
