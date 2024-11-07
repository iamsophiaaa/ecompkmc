# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm ,LoginForm # Assume you've created a LoginForm for login
from .models import CustomerProfile, SellerProfile

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to homepage or dashboard
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user first
            if user.user_type == 'customer':
                CustomerProfile.objects.create(user=user)
            elif user.user_type == 'seller':
                SellerProfile.objects.create(user=user)

            login(request, user)  # Log the user in after registration
            return redirect('login')  # Redirect to home or customer dashboard
    else:
        form = RegistrationForm()
    return render(request, 'account/register_user.html', {'form': form})

# accounts/views.py

