from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, SellerProfile, CustomerProfile

from django.contrib.auth import get_user_model

User = get_user_model()

class RegistrationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES, required=True)
    

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'department', 'address', 'contact_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['autocomplete'] = 'new-password'
        self.fields['password2'].widget.attrs['autocomplete'] = 'new-password'

    

    def save(self, commit=True):
        # Create user instance
        user = super().save(commit=False)
        user.user_type = self.cleaned_data['user_type']
     
        
        if commit:
            # Save the user first
            user.save()

            # Create the appropriate profiles based on the user type
            if user.user_type == 'seller':
                # Create SellerProfile
                SellerProfile.objects.create(user=user, department=user.department)
            elif user.user_type == 'customer':
                # Create CustomerProfile
                CustomerProfile.objects.create(user=user, department=user.department)
            elif user.user_type == 'both':
                # Create both profiles
                SellerProfile.objects.create(user=user, department=user.department)
                CustomerProfile.objects.create(user=user, department=user.department)

        return user




class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    