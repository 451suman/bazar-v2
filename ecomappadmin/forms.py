from django import forms

from ecomapp.models import Category, Product
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
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

    def clean_title(self):
        clean_title = self.cleaned_data["title"]
        if Category.objects.filter(title=clean_title).exists():
            raise forms.ValidationError("Category with this title already exists.")
        return clean_title