# Generated by Django 4.1.5 on 2023-02-10 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_ordervehicle_vehicles'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='booking_amount',
            field=models.BigIntegerField(default=0),
        ),
    ]