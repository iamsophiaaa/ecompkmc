from django.shortcuts import render
def cart_summary(request):
 return render (request,"cart_summary.html",{})

def cart_add(request):
 return render(request,"cart_add.html",{})