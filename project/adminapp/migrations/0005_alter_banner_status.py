# Generated by Django 4.1.5 on 2023-03-12 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0004_banner_texts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='status',
            field=models.CharField(choices=[('None', 'None'), ('Active', 'Active'), ('De-Active', 'De-Active')], default='None', max_length=100),
        ),
    ]