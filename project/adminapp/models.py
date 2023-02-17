from django.db import models

# Create your models here.


class Banner(models.Model):
    Description=models.CharField(max_length=500,blank=True)
    image = models.ImageField(upload_to='photos/Banners')
