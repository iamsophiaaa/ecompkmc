from django.urls import path
from . import views

urlpatterns =[
    path('', views.home, name='home'),
    path('second_hand/', views.second, name='second'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    # path('register/', views.register_user, name='register'),
    path('product/int<pk>', views.product, name='product'),
    path('category/<str:co>', views.category, name='category'),
     path('search/', views.search, name='search'),

]   
