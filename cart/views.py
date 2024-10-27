from django.shortcuts import render,get_object_or_404
from .cart import Cart
from core.models import Product
from django.http import JsonResponse
def cart_summary(request):
    cart = Cart(request)  # Instantiate Cart with the request
    cart_products = cart.get_products()  # Call the method to get products
    return render(request, "cart_summary.html", {"cart_products": cart_products})


def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('productId')

        # Initialize cart in session if it doesn't exist
        if 'cart' not in request.session:
            request.session['cart'] = {}

        cart = request.session['cart']

        # If the product is already in the cart, increment its quantity
        if product_id in cart:
            cart[product_id]['qty'] += 1
        else:
            # Add the product to the cart with an initial quantity of 1
            product = Product.objects.get(id=product_id)
            cart[product_id] = {
                'name': product.name,
                'price': str(product.price),  # Store price as string to avoid serialization issues
                'qty': 1
            }

        # Save back to the session
        request.session['cart'] = cart
        request.session.modified = True

        # Calculate total quantity
        total_quantity = sum(item['qty'] for item in cart.values())
        return JsonResponse({'cart_quantity': total_quantity})

    return JsonResponse({'error': 'Invalid request'}, status=400)
