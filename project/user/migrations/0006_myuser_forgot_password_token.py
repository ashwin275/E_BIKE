# Generated by Django 4.1.5 on 2023-01-25 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_userdetail_default'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='forgot_password_token',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
