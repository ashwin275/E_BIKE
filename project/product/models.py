from django.db import models

# Create your models here.
from user.models import myuser
from categories.models import Category
from datetime import datetime
from django.utils import timezone
# Create your models here.

class Vehicles(models.Model):
    vehicle_name =models.CharField(max_length=200,unique=True)
    vendor_id = models.ForeignKey(myuser,on_delete=models.CASCADE,default=None)
    slug = models.SlugField(max_length=200,unique=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)#unique =TRUE
    range = models.CharField(max_length=5)
    top_speed = models.IntegerField()
    image = models.ImageField(upload_to='photos/vehicles')
    created_date =models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)
    gif_image_vehicle = models.URLField(max_length=200, null=True, default=None)
   
    def reviews(self):
        average = 0
        review = Review.objects.filter(product = self)
        count = review.count()
        
        for i in review:
            average += i.rating

        try:
            average = average/count

        except:
            average = 0
        return round(average)

    def review_count(self):
        return  Review.objects.filter(product = self).count()


    def __str__(self) :
        return self.vehicle_name




class Variant(models.Model):
    vehicle_id = models.ForeignKey(Vehicles,on_delete=models.CASCADE)
    image1 = models.ImageField(upload_to='photos/vehicles')
    image2 = models.ImageField(upload_to='photos/vehicles')
    image3 = models.ImageField(upload_to='photos/vehicles')
    price = models.IntegerField()
    remaining = models.IntegerField()
    is_available = models.BooleanField(default=True)
    color  =models.CharField(max_length=100,default='#FF0000')
   

    def __str__(self):
        return self.vehicle_id.vehicle_name


class Review(models.Model):
    user = models.ForeignKey(myuser, on_delete=models.CASCADE)
    product = models.ForeignKey(Vehicles, on_delete=models.CASCADE)
    review = models.TextField(max_length=300)
    rating = models.IntegerField()
    created_date = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=50,null=True)


    def __str__(self):
        return self.product.vehicle_name