from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('switch_role/', views.switch_role, name='switch_role'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('profile/edit/<int:user_id>/', views.edit_profile, name='edit_profile'),
]