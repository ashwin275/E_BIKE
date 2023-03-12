from django.db import models

# Create your models here.

banner = (
    ('None','None'),
    ('Active','Active'),
    ('De-Active','De-Active'),
)

class Banner(models.Model):
    Description=models.CharField(max_length=500,blank=True)
    texts = models.CharField(max_length=500,blank=True,null=True)
    image = models.ImageField(upload_to='photos/Banners')
    status=models.CharField(max_length=100,  choices=banner,default='None')

