from django.urls import path
# Create your views here.
def home(request):
    return render(request, 'home.html', {})
