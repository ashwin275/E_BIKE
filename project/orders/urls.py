from django.urls import path
from .import views



app_name = 'Orders'

urlpatterns = [
      
      path('order_success',views.Book_now,name="Book_now"),
      path('handlerrequest',views.handlerrequest,name="handlerrequest"),
      path('paymentfailed',views.payment_failed,name='payment_failed')

]