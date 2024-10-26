# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, SellerProfile, CustomerProfile


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'password1', 'password2', 'role', 'address', 'contact_number']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'customer'
        if commit:
            user.save()
        return user





class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)