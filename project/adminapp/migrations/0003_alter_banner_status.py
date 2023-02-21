# Generated by Django 4.1.5 on 2023-02-21 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0002_banner_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='status',
            field=models.CharField(choices=[('None', 'None'), ('Banner-one', 'Banner-one'), ('Banner-two', 'Banner-two')], default='None', max_length=100),
        ),
    ]
