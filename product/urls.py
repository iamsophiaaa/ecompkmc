# products/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search, name='product_search'),
]
