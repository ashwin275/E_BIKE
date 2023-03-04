from django.db import models
from user.models import myuser
from product.models import Variant

# Create your models here.

class Cart(models.Model):
    cart_id=models.CharField(max_length=250,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)
    
    
    def __int__(self):
         return self.cart_id
    
    # def __str__(self):
    #     return self.cart_id
    



class CartItem(models.Model):
    user = models.ForeignKey(myuser, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Variant, on_delete=models.CASCADE)
   
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)


    def sub_total(self):
        return self.product.price*self.quantity
    
    
    

    
class Coupon(models.Model):
    coupon_code = models.CharField(max_length=10,blank=True)
    discount = models.FloatField()
    is_active = models.BooleanField(default=True)
   


    def __str__(self):
        return self.coupon_code


class Used_Coupon(models.Model):
    user = models.ForeignKey(myuser,on_delete=models.CASCADE,null=True)
    coupon = models.ForeignKey(Coupon,on_delete=models.CASCADE,null=True)