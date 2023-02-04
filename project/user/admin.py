from django.contrib import admin
from django.db.models.base import Model
from .models import myuser,Userdetail

# Register your models here.

admin.site.register(myuser)
admin.site.register(Userdetail)