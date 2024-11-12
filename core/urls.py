from django.urls import path
from . import views


app_name = 'core'
urlpatterns =[
    path('', views.home, name='home'),
    path('second_hand/', views.second, name='second'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    # path('register/', views.register_user, name='register'),
    path('product/int<pk>', views.product, name='product'),
    path('category/<str:co>', views.category, name='category'),
    # path('search/', views.search, name='search'),
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),
    # path('products/', views.product_list, name='product_list'),
    # path('place_order/', views.place_order, name='place_order'),
    # path('order_success/', views.order_success, name='order_success'),

]   
