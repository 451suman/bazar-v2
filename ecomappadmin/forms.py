from django import forms

from ecomapp.models import Product
from django_summernote.widgets import SummernoteWidget


class AdminLoginForm(forms.Form):
    username = forms.CharField(max_length=150, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

        widgets = {
            "description": SummernoteWidget(),
        }
