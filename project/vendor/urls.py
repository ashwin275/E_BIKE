from django.urls import path
from .import views

app_name = 'vendor'

urlpatterns = [
    path('',views.vendor_register,name='vendor_register'),
    path('verifyvender',views.verify_vender,name='verify_vender'),
    path('vendor-signin',views.vendor_signin,name='vendor_signin'),
    path('vendor_logout',views.vendor_logout,name='vendor_logout'),
    path('vendordashboard',views.vendor_dashboard,name='vendor_dashboard'),
    path('vendor_profile',views.vendor_profile,name='vendor_profile'),


    path('viewvehicles',views.view_vehicles,name='view_vehicles'),
    path('non-available-vehicles',views.Non_Available_vehicles,name='Non_Available_vehicles'),
    path('addvehicle',views.add_vehicles,name='add_vehicle'),
    path('editvehicle/<int:pk>',views.edit_vehicle,name='edit_vehicle'),
    path('deletevehicle/<int:pk>',views.delete_vehicle,name='delete_vehicle'),
    path('activevehicle/<int:pk>',views.active_vehicle,name='active_vehicle'),
    path('deactivevehicle/<int:pk>',views.deactive_vehicle,name='deactive_vehicle'),

    path('addvariant/<int:pk>',views.add_variant,name='add_variant'),
    path('viewvariant/<int:pk>',views.view_variant,name='view_variant'),
    path('edit-variant/<int:pk>',views.edit_variant,name='edit_variant'),
    path('delete-variant/<int:pk>',views.delete_variant,name='delete_variant'),
    path('active-variant/<int:pk>',views.active_variant,name='active_variant'),
    path('de-activevariant/<int:pk>',views.de_active_variant,name='de_active_variant'),

    path('Orders',views.Orders,name='Orders'),
    path('cancel-order/<int:pk>',views.cancel_order,name='cancel_order'),
    path('order_detail/<int:pk>',views.order_details,name='order_details'),
   


]