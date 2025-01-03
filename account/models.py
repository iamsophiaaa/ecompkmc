from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('seller', 'Seller'),
        ('both', 'Both')
    )
    active_role = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='seller')  # Field to store the active role
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='customer')
    username = models.CharField(max_length=50, blank=False, null=False, unique=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    contact_number = models.CharField(max_length=10,  blank=True, null=True)

    DEPARTMENT_CHOICES = (
        ('', 'Select'),
        ('bca', 'BCA'),
        
        ('bit', 'BIT'),
    )
    department = models.CharField(max_length=10, choices=DEPARTMENT_CHOICES,   null=False, default="bca")  


    def switch_role(self):
        
        if self.user_type == 'both':
            if self.active_role == 'seller':
                self.active_role = 'customer'
            else:
                self.active_role = 'seller'
            self.save()
        else:
            raise ValueError("User must have 'both' roles to switch between them.")

class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.CharField(max_length=10, choices=User.DEPARTMENT_CHOICES, null=False, default="bca")
    def __str__(self):
        return self.user.username
    # Additional fields specific to customers, e.g., preferences, order history, etc.

class SellerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.CharField(max_length=10, choices=User.DEPARTMENT_CHOICES, null=False, default="bca")
    def __str__(self):
        return self.user.username
    # Additional fields specific to sellers, e.g., store name, products, etc.
