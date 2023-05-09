from django.db import models
import uuid
from product.models import Vehicles
from user.models import myuser
# Create your models here.

class Offers(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor=models.ForeignKey(myuser,on_delete=models.CASCADE,null=True)
    vehicle = models.OneToOneField(Vehicles, on_delete=models.CASCADE,unique=True)
    discount = models.PositiveIntegerField(help_text='Offer in percentage',default=0)
    is_active = models.BooleanField(default=True)
    

    def __str__(self):
        return str(self.discount)