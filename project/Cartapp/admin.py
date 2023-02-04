from django.contrib import admin
from.models import Cart,CartItem,Coupon,Used_Coupon

# Register your models here.

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Coupon)
admin.site.register(Used_Coupon)
