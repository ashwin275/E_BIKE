# Generated by Django 4.1.5 on 2023-06-10 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_review_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicles',
            name='gif_image_vehicle',
            field=models.URLField(default=None, null=True),
        ),
    ]