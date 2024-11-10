from core.models import Product, Category
from account.models import SellerProfile
from django import forms
from django.core.exceptions import ValidationError
import os


def validate_image_extension(value):
    valid_extensions = ['.jpg', '.jpeg', '.png']
    ext = os.path.splitext(value.name)[1]  # Get file extension
    if ext.lower() not in valid_extensions:
        raise ValidationError("Invalid file extension. Allowed extensions are: .jpg, .jpeg, .png")
    
def clean_image(self):
    image = self.cleaned_data.get('image')
    if image:
        # Check file size manually (e.g., limit to 5MB)
        max_size = 5 * 1024 * 1024  # 5 MB in bytes
        if image.size > max_size:
            raise ValidationError("File size must not exceed 5 MB.")
    return image

class AddProduct(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter product name" , "class": "form-control"}))
    description = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter product description" , "class": "form-control"}))
    price = forms.IntegerField(widget=forms.NumberInput(attrs={ "class": "form-control"}))
    number = forms.IntegerField(widget=forms.NumberInput(attrs={ "class": "form-control"}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select")
    image = forms.ImageField(required=True, widget=forms.ClearableFileInput(attrs={"class": "form-control-file"}))
    
    class Meta:
        model= Product
        fields = [
            'name', 
            'image', 
            'description',
            'price',
            'condition',
            'number',
            'category',
            'image',
            

        ]
    def save(self, commit=True, user=None):
        # Save the form instance first
        product = super().save(commit=False)

        if user:
            # Set the current logged-in user as the seller
            print(f"Saving product with seller: {user.sellerprofile}")
            seller_profile = user.sellerprofile  # Assumes there's a SellerProfile related to the User
            product.seller = seller_profile
        
        if commit:
            try:
                product.save()  # Try saving the product to the database
            except Exception as e:
                print(f"Error saving product: {e}")
                raise
        
        return product
