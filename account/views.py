# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm ,LoginForm , UserProfileForm# Assume you've created a LoginForm for login
from .models import CustomerProfile, SellerProfile, User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You are now logged in.")
                if user.user_type=='customer' :

                    return redirect('core:customer_dashboard')  # Redirect to homepage or dashboard
                elif user.user_type=='seller'or user.user_type=='both':

                    return redirect('core:seller_dashboard') 
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})



def register(request):
    if request.method == 'POST':
        print("POST request received")  # Debugging print statement
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            print("Form is valid")  # Debugging print statement
            try:
                user = form.save()

                # Check if the user is of type 'customer' or 'both'
                
                if user.user_type == 'seller':
                    # Check if the SellerProfile already exists
                    if not hasattr(user, 'sellerprofile'):  # Check if the profile already exists
                        # Create SellerProfile (department is part of User)
                        SellerProfile.objects.create(user=user)
                    else:
                        # Optionally, update the existing SellerProfile
                        user.sellerprofile.save()
                elif user.user_type == 'customer':
                    # Check if the CustomerProfile already exists
                    if not hasattr(user, 'customerprofile'):  # Check if the profile already exists
                        # Create CustomerProfile
                        CustomerProfile.objects.create(user=user)
                    else:
                        # Optionally, update the existing CustomerProfile
                        user.customerprofile.save()
                elif user.user_type == 'both':
                    # Create both SellerProfile and CustomerProfile
                    if not hasattr(user, 'sellerprofile'):  # Check if SellerProfile exists
                        SellerProfile.objects.create(user=user)
                    if not hasattr(user, 'customerprofile'):  # Check if CustomerProfile exists
                        CustomerProfile.objects.create(user=user)
                    

                # Log the user in after successful registration
                login(request, user)
                
                # Redirect to login or another appropriate page
                messages.success(request, "Registration successful! You are now logged in.")
                return redirect('account:login')  # or another URL if necessary
                
            except Exception as e:
                print(f"Error occurred: {str(e)}")
                messages.error(request, f"An error occurred: {str(e)}")
                return redirect('account:register')
        else:
            print("Form is invalid")  # Debugging print statement
            messages.error(request, "Please correct the errors below.")
    else:
        print("GET request received")  # Debugging print statement
        form = RegistrationForm()

    return render(request, 'account/register_user.html', {'form': form})

@login_required
def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
     # Get the currently logged-in user
    return render(request, 'account/profile.html', {'user': user})

@login_required
def edit_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('account:profile', user_id=user.id)  # Redirect to the profile page after saving
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'account/edit_profile.html', {'form': form, 'user': user})

@login_required
def switch_role(request):
    user = request.user

    # Check if the user has both roles
    if user.user_type == 'both':
        # Switch between roles based on the current active role
        if user.active_role == 'customer':
            user.active_role = 'seller'
        else:
            user.active_role = 'customer'
        user.save()

    # Redirect the user based on their active role
    if user.active_role == 'customer':
        return redirect('core:customer_dashboard')
    else:
        return redirect('core:seller_dashboard')
