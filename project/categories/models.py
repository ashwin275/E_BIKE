from django.db import models

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=50,unique=True)
    description = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50,unique=True)
    image = models.ImageField(upload_to='category' ,default='',null=True)
    gif_image = models.URLField(max_length=200, null=True, default=None)

    
    

    
    class meta:
        verbose_name = 'Category'
        verbose_name_plural = 'categories'
    def __str__(self):
        
        return self.category_name