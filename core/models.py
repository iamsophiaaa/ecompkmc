import datetime
from django.conf import settings
from django.db import models
from django.contrib.auth.models import PermissionsMixin,BaseUserManager, AbstractBaseUser

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
# class CustomUserManager(BaseUserManager):
#     def get_by_natural_key(self, username):
#         return self.get(username=username)
class Seller(models.Model):
    
    username= models.CharField(max_length=50, unique="true")
    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email'] 
    # objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class Product(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('second_hand', 'Second_Hand'),
       
    ]
    name = models.CharField(max_length=50)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default= 1)
    image = models.ImageField(upload_to='uploads/product')
    description =models.CharField(max_length=200, default='', blank=True, null=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE , default=1) 
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='new')
    

    
    def __str__(self):
        return self.name
    
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    phone =  models.CharField(max_length=20, default='', blank=True )
    address = models.CharField(max_length=100, default='', blank=True )
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
       return f'Order for {self.product.name} by {self.customer.first_name}'

    
