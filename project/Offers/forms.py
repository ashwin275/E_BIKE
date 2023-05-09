
from django import forms
from .models import Offers


class Reviewforms(forms.ModelForm):
    class Meta:
        model = Offers
        fields = ('discount','is_active')
