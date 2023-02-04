from django.forms import ModelForm
from django import forms
from user.models import Userdetail



class AddressForm(ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=50)
    addressline1=forms.CharField(max_length=100)
    addressline2=forms.CharField(max_length=100)
    city=forms.CharField(max_length=100)
    state=forms.CharField(max_length=50)
    country=forms.CharField(max_length=50)
    mobile=forms.CharField(max_length=10)
   
 
    
    class Meta:
        model = Userdetail
        exclude = ['user_id']