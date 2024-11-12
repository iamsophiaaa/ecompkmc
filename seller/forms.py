from core.models import Product
from django import forms


class AddProduct(forms.ModelForm):

    class Meta:
        model= Product
        fields = [
            'title', 
            'image', 
            'description',
            'price',
            'category',
            'number',
            'condition',

        ]