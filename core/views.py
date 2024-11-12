from django.shortcuts import render, redirect
from .models import Product,Category,  Order

from django.contrib.auth import authenticate , login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from account.models  import SellerProfile, CustomerProfile
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from cart.models import Cart, CartItem 

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

        








def logout_user(request):
    logout(request)
    messages.success(request, ("You've been logged out."))
    return redirect('core:home')

def register_user(request):
   
    return render(request, 'account/register_user.html', {})




def customer_dashboard(request):
    user  = request.user
    try:
        customer_profile = CustomerProfile.objects.get(user=user)
    except CustomerProfile.DoesNotExist:
        customer_profile = None  # Or handle this case if the user is not a seller

    # If the seller profile exists, filter the products by the seller's profile
    if customer_profile:
        products = Product.objects.all()
        
        user_department = user.department
        sellers = SellerProfile.objects.filter(department = user_department)
        if sellers.exists():
            products_from_same_department = Product.objects.filter(seller__in=sellers)
        else:
            # If no sellers are found in the same department, return an empty queryset
            products_from_same_department = Product.objects.none()
    else:
        # If there's no customer profile, return no products
        products = Product.objects.none()
        products_from_same_department = Product.objects.none()
    
    return render(request, 'core/customer_dash.html', {'products': products, 'products_from_same_department': products_from_same_department})
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
        orders = Order.objects.filter(items__product__in=products).distinct()
    else:
        products = Product.objects.none()
    
    
    return render(request, 'core/seller_dash.html', {'products': products, 'orders': orders})



# def product_list(request):
#     user = request.user
#     seller_profile = SellerProfile.objects.get(user=user)
#     products = Product.objects.filter(seller=seller_profile)
    

#     return render(request, 'core/product_list.html', {'products': products})


