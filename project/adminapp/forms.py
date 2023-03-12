from django import forms
from Cartapp.models import Coupon
from.models import Banner



class Couponforms(forms.ModelForm):

    class Meta:
        model = Coupon
        fields = ('coupon_code','discount',) 


class Bannerforms(forms.ModelForm):

    class Meta:
        model = Banner
        fields = ('Description','image','status','texts')

    