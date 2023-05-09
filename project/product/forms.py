# from django.forms import ModelForm
from django import forms
from .models import Vehicles , Variant,Review


class Vehicleforms(forms.ModelForm):

    class Meta:
        model = Vehicles
        fields = ('vehicle_name','slug','category','range','top_speed','image')


class Variantform(forms.ModelForm):
    class Meta:
        model = Variant
        fields = ('image1','image2','image3','price','remaining','is_available','color')
  

class Reviewforms(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('review','rating','subject')


