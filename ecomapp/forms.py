from django import forms
from .models import Customer, Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomerRegistrationsForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())
    class Meta:
        model = Customer
        fields =["username","password","email","full_name", "address", ]

    def clean_username(self):
        uname = self.cleaned_data.get("username")
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError(
                "Customer with this username already exists.")

        return uname
    
    def clean_email(self):
        uemail = self.cleaned_data.get("email")
        if User.objects.filter(email=uemail).exists():
            raise forms.ValidationError(
                "Customer with this email already exists.")

        return uemail



class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields =["ordered_by","shipping_address","mobile","email"]

    def clean_mobile(self):
        mob = self.cleaned_data["mobile"]
        if len(mob) != 10:
            raise forms.ValidationError("Mobile number must be exactly 10 digits.")
        return mob

class CustomerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())