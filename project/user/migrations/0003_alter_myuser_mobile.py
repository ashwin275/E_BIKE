# Generated by Django 4.1.5 on 2023-01-15 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_remove_myuser_gst_number_myuser_gst_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='mobile',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
