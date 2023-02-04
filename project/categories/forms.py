from django import forms
from .models import Category


class categoryform(forms.ModelForm):
    class Meta:
        model = Category
        fields =('category_name','slug','description','image')
