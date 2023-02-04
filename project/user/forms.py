#from django import forms
from .models import Userdetail
from django.forms import ModelForm



class userdetail(ModelForm):
    class Meta:
        model = Userdetail

        fields = ['first_name','last_name','email','mobile','addressline1','addressline2','city','state','country']






