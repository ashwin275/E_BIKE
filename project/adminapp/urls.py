from django.urls import path
from .import views



urlpatterns = [
    path('',views.admin_signin,name='admin_signin'),
    path('adminpanel',views.admin_panel,name='admin_panel'),
    path('adminlogout',views.admin_logout,name='admin_logout'),
    
    path('vendormgmt',views.vendor_mgmt,name='vendor_mgmt'),
    path('blockvendor/<int:pk>',views.block_vendor,name='block_vendor'),
    path('unblockvendor/<int:pk>',views.unblock_vendor,name='unblock_vendor'),
    path('deletevendor/<int:pk>',views.delete_vendor,name='delete_vendor'),

    path('usermgmt',views.user_mgmt,name='user_mgmt'),
    path('unblockuser/<int:id>',views.unblock_user,name='unblock_user'),
    path('blockuser/<int:pk>',views.block_user,name='block_user'),
    path('deleteuser/<int:pk>',views.delete_user,name='delete_user'),


    path('category',views.view_category,name='view_category'),
    path('deletecategory/<int:pk>',views.delete_category,name='delete_category'),
    path('addcategory',views.add_category,name='add_category'),
    path('editcategory/<int:pk>',views.edit_category,name='edit_category'),

]