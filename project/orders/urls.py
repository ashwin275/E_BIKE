from django.urls import path
from .import views



app_name = 'Orders'

urlpatterns = [
      
      path('Book_now',views.Book_now,name="Book_now")

]