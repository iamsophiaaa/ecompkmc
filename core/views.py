from django.shortcuts import render, redirect
from .models import Product,Category
from django.contrib.auth import authenticate , login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from account.models  import SellerProfile
# from django import forms
# from .forms import SignUpForm
import os
from django.conf import settings
# Create your views here.
def category(request,co):
    co=co.replace('-' ,'')
    category = Category.objects.get(name=co)
    products=Product.objects.filter(category=category)
    return render(request, 'core/category.html', {'products':products,'category':category})

def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'core/product.html', {'product':product,})

    
def home(request):
    products = Product.objects.all()

    return render(request, 'core/home.html', {'products':products})

def second(request):
    products = Product.objects.filter(condition='second_hand')
    return render(request, 'core/home.html', {'products':products})


def about(request):
    return render(request, 'core/about.html', {})

        


# def register_user(request):
#     form = SignUpForm()
#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password1']
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             messages.success(request, ("You've registered successfully"))
#             return redirect('login')
#         else:
#             messages.error(request, "oops there was problem in registering , please try again!!!")
#             return redirect('register')
#     else:
#         return render(request, 'register_user.html', {'form':form})


def login_user(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request , username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You've been logged in successfully"))
            if user=='customer':
                return redirect('customer_dashboard')
            
            elif user=='seller':
                return redirect('seller_dashboard')
        else:
            messages.success(request, ("There was an error"))
            return redirect('login')
    
    else:
        return render(request, 'login.html', {})
        
        



    



def logout_user(request):
    logout(request)
    messages.success(request, ("You've been logged out."))
    return redirect('home')

def register_user(request):
   
    return render(request, 'register_user.html', {})


def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        return render(request,"search.html", {'searched':searched} )
    else:
        return render(request, "core/search.html", {})


def customer_dashboard(request):
   
    return render(request, 'core/customer_dash.html', {})

def seller_dashboard(request):
    user = request.user
    
    # Get the SellerProfile related to the logged-in user
    try:
        seller_profile = SellerProfile.objects.get(user=user)
    except SellerProfile.DoesNotExist:
        seller_profile = None  # Or handle this case if the user is not a seller

    # If the seller profile exists, filter the products by the seller's profile
    if seller_profile:
        products = Product.objects.filter(seller=seller_profile)
    else:
        products = Product.objects.none()
    
    
    return render(request, 'core/seller_dash.html', {'products': products})