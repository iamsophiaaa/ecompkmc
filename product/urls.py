# products/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search, name='product_search'),
    path('add_products/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    

]
