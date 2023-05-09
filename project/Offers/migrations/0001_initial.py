# Generated by Django 4.1.5 on 2023-03-26 09:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0006_alter_review_rating'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Offers',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('discount', models.PositiveIntegerField(default=0, help_text='Offer in percentage')),
                ('is_active', models.BooleanField(default=True)),
                ('vehicle', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='product.vehicles')),
                ('vendor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
