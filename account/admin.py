
from django.contrib import admin
from .models import User, CustomerProfile, SellerProfile

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'user_type', 'department']

class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'department']  # Customize as needed

    def first_name(self, obj):
        return obj.user.first_name
    
    def last_name(self, obj):
        return obj.user.last_name


    def department(self, obj):
        return obj.user.department

    

class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'department']  # Customize as needed

    def first_name(self, obj):
        return obj.user.first_name
    
    def last_name(self, obj):
        return obj.user.last_name


    def department(self, obj):
        return obj.user.department

admin.site.register(User, UserAdmin)
admin.site.register(CustomerProfile, CustomerProfileAdmin)
admin.site.register(SellerProfile, SellerProfileAdmin)
