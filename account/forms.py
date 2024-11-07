# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, SellerProfile, CustomerProfile



from django.contrib.auth import get_user_model

User = get_user_model()




class RegistrationForm(UserCreationForm):

    password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'password1', 'password2', 'user_type', 'address', 'contact_number']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user





class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)