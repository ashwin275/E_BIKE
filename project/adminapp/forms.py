from django import forms
from Cartapp.models import Coupon



class Couponforms(forms.ModelForm):

    class Meta:
        model = Coupon
        fields = ('coupon_code','discount',) 
    