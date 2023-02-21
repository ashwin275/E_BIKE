from django.db import models

# Create your models here.

banner = (
    ('None','None'),
    ('Banner-one','Banner-one'),
    ('Banner-two','Banner-two'),
)

class Banner(models.Model):
    Description=models.CharField(max_length=500,blank=True)
    image = models.ImageField(upload_to='photos/Banners')
    status=models.CharField(max_length=100,  choices=banner,default='None')

