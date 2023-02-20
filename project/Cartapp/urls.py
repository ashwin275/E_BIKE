from django.urls import path
from .import views
from .views import *
#from user.views import *

app_name = 'Cartapp'

urlpatterns = [
    path('',views.cart,name='cart'),
    path('add_to_cart/<int:pk>',views.add_to_cart,name='add_to_cart'),
    path('remove_cart_item/<int:pk>',views.remove_cart_item,name='remove_cart_item'),
    path('decrement_quantity/<int:pk>',views.decrement_quantity,name='decrement_quantity'),
    path('checkout',views.checkout,name='checkout'),
    path('adress_default/<int:id>',views.address_default,name='address_default'),
    path('review_order', views.review_order,name="review_order"),

    path('coupon_apply',views.coupon_apply,name='coupon_apply'),
    path('cancel_coupon',views.cancel_coupon,name='cancel_coupon'),
    path('cart-count',views.cart_count,name='cart_count'),
 
   path('update_cart_quantity',views.update_cart_quantity,name='update_cart_quantity')

]