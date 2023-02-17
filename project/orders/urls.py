from django.urls import path
from .import views



app_name = 'Orders'

urlpatterns = [
      
      path('order_success',views.Book_now,name="Book_now"),
      path('handlerrequest',views.handlerrequest,name="handlerrequest"),
      
      path('download_invoice/<int:id>',views.download_invoice,name="download_invoice"),

]