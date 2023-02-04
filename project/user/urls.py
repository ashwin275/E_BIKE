
from django.urls import path
from .import views
from .views import *
#from user.views import *

app_name = 'user'

urlpatterns = [
    path('userregister',views.user_register,name='user_register'),
    path('usersignin',views.user_signin,name='user_signin'),
    path('',views.home,name='home'),
    path('verify-otp',views.verify_otp,name='verify_otp'),
    path('home',views.home,name='home'),
    path('logout-user',views.logout_user,name='logout_user'),

    path('singleproducts/<int:pk>',views.single_products,name='single_products'),
    path('Shop',views.Shop,name='Shop'),
         
   # path('Userdetail',Userdetail.as_view(),name='Userdetail'),
   # path('userprofile',user_profile.as_view(),name='user_profile'),

     path('userprofile',views.user_profile,name='user_profile'),
    path('addaddress',views.add_address,name='add_address'),
    path('deleteaddress/<int:pk>',views.delete_address,name='delete_address'),
    path('editaddress/<int:pk>',views.edit_address,name='delete_address'),
    path('forgot_password',views.forgot_password,name='forgot_password'),
    path('changepassword/<token>/',views.change_password,name='change_password'),


    path('view_orders',views.view_orders,name='view_orders'),
    path('cancel_order/<int:pk>',views.cancel_order,name="cancel_order"),
    path('order_details/<int:pk>',views.order_details,name='order_details'),


]