from django.urls import path
from . import views

urlpatterns =[
     path('', views.cart_summary, name='cart_summary'),
     # path('', views.index, name='cart_index'),
      path('add/', views.add_to_cart, name='add_to_cart'),
      #path('delete/',views.cart_delete,name="cart_delete") ,
      #path('update/',views.cart_update,name="cart_update") ,

]