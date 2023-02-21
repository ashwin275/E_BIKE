from django.urls import path
from .import views



urlpatterns = [
    path('',views.admin_signin,name='admin_signin'),
    path('adminpanel',views.admin_panel,name='admin_panel'),
    path('filter_admin_dashboard',views.filter_admin_dashboard,name='filter_admin_dashboard'),
    path('sales_report',views.sales_report,name='sales_report'),
    path('excel',views.Excel_sales_report,name='Excel_sales_report'),
    path('adminlogout',views.admin_logout,name='admin_logout'),
    path('pdf_sales',views.pdf_sales,name='pdf_sales'),
   # path('filter_sales',views.filter_sales_report,name='filter_sales_report'),
    
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

    path('view-coupons',views.view_coupon,name='view_coupon'),
    path('add-coupons',views.add_coupons,name='add_coupons'),
    path('block/<int:id>',views.block_coupon,name='block_coupon'),
    path('un-block/<int:id>',views.un_block_coupon,name='un_block_coupon'),
    path('delete-coupon/<int:id>',views.del_coupon,name='del_coupon'),

    path('add-banner',views.add_banner,name='add_banner'),
    path('view-banner',views.view_banner,name='view_banner'),
    path('delete-banner/<int:id>',views.delete_banner,name='delete_banner'),
    path('update-banner/<int:id>',views.update_banner,name='update_banner'),

    # path('banner-status/<int:id>',views.banner_status_change_main,name='banner_status_change_main'),
    # path('banner-two/<int:id>',views.banner_status_change_sub,name='banner_status_change_sub'),

]