from django.urls import path
from core import views
app_name="url"
urlpatterns=[
    path("url/", views.index)
]