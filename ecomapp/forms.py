from django import forms
from .models import Contact, Customer, Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomerRegistrationsForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())
    class Meta:
        model = Customer
        fields =["username","password","email","full_name", "address","mobile" ]

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
    
def clean_mobile(self):
    mob = self.cleaned_data.get("mobile")
    
    # Check if the mobile number is numeric
    if not mob.isdigit():
        raise forms.ValidationError("Mobile number must contain only digits.")
    
    # Check if the mobile number is already registered
    if User.objects.filter(mobile=mob).exists():
        raise forms.ValidationError("Mobile Number already registered in the system.")
    
    return mob




class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields =["customer","ordered_by","shipping_address","mobile","email"]

    def clean_mobile(self):
        mob = self.cleaned_data["mobile"]
        if len(mob) != 10:
            raise forms.ValidationError("Mobile number must be exactly 10 digits.")
        return mob

class CustomerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['subject', 'message']  # Only include subject and message in the form
