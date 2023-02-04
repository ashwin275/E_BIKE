# from django.forms import ModelForm
from django import forms
from .models import Vehicles


class Vehicleforms(forms.ModelForm):

    class Meta:
        model = Vehicles
        fields = ('vehicle_name','slug','category','range','top_speed','image','image1','image2','image3','price','remaining')

  