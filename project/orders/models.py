from django.db import models
from user.models import myuser,Userdetail
from Cartapp.models import CartItem
from product.models import Vehicles,Variant

# Create your models here.


STATUS = (
        ('Confirmed','Confirmed'),
        ('Shipped','Shipped'),
        ('Out_for_delivery','Out_for_delivery'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
        ('Returned','Returned'),
        
    )

PAYMENTS=(
       
        ('razorpay','razorpay'),
        ('COD','COD'),
    )

class Orders(models.Model):

    user =models.ForeignKey(myuser,on_delete=models.CASCADE)
    address =models.ForeignKey(Userdetail,on_delete=models.CASCADE)
    order_number=models.CharField(max_length=20)
    order_total=models.FloatField(default=1)
    payment_option=models.CharField(max_length=30, choices=PAYMENTS, null=True,blank=True)
    pending_amount=models.BigIntegerField(default=0)
    tax=models.FloatField()
    discount_price=models.FloatField(default=0)
    status=models.CharField(max_length=100,default='Confirmed')
    is_ordered=models.BooleanField(default=False)   
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    booking_amount = models.BigIntegerField(default=0)

class OrderVehicle(models.Model):
    order = models.ForeignKey(Orders,on_delete=models.CASCADE)
    vehicles = models.ForeignKey(Variant,on_delete=models.CASCADE)
    quantity =   models.IntegerField(null=True)
    price   =   models.FloatField(max_length=200,null=True)
    status  =   models.CharField(max_length=30, choices=STATUS, default='Confirmed')
    ordered=models.BooleanField(default=False)
    user=models.ForeignKey(myuser,on_delete=models.CASCADE)

    def sub_total(self):
        return self.price*self.quantity

class Payment(models.Model):
    user =  models.ForeignKey(myuser,on_delete=models.CASCADE, null=True)
    payment_id = models.CharField(max_length=100,null=True,blank=True)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name        ='payment'
        verbose_name_plural ='payments'
        
    def __str__(self):
        return self.payment_method
