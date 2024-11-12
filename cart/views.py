from django.shortcuts import render,get_object_or_404,redirect
from .cart import Cart
from core.models import Product,Order
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
def cart_summary(request):
    cart_products = []
    cart = request.session.get('cart', {})

    # Handle the form submission for updating the quantity
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        new_quantity = int(request.POST.get('quantity'))

        # Update the quantity if the product is in the cart
        if product_id in cart:
            cart[product_id]['qty'] = new_quantity
            request.session['cart'] = cart  # Save the updated cart back to the session
            messages.success(request,("Product updated..."))

    # Handle the deletion of a product from the cart
    if request.method == 'POST' and 'delete' in request.POST:
        product_id = request.POST.get('product_id')

        # Remove the product from the cart if it exists
        if product_id in cart:
            del cart[product_id]
            request.session['cart'] = cart  # Save the updated cart back to the session
       
        return redirect('cart_summary')  # Redirect to the same page to refresh the cart

    # Populate the cart_products list with product details and quantities
    for product_id, item in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            cart_products.append({
                'product': product,
                'quantity': item['qty']
            })
        except Product.DoesNotExist:
            continue

    total_quantity = sum(item['quantity'] for item in cart_products)
    total_price = sum(float(item['product'].price) * item['quantity'] for item in cart_products)

    context = {
        'cart_products': cart_products,
        'total_quantity': total_quantity,
        'total_price': total_price
    }

    return render(request, 'cart_summary.html', context)

def add_to_cart(request):
    if request.method == 'POST':
        # Retrieve product_id and quantity from the AJAX request
        product_id = request.POST.get('productId')
        quantity = int(request.POST.get('quantity', 1))  # Default to 1 if quantity is not provided

        # Retrieve the product or return 404 if it doesn't exist
        product = get_object_or_404(Product, id=product_id)

        # Initialize the cart in the session if it doesn't exist
        if 'cart' not in request.session:
            request.session['cart'] = {}

        cart = request.session['cart']

        # Add or update the product quantity in the cart
        if product_id in cart:
            cart[product_id]['qty'] += quantity
        else:
            cart[product_id] = {
                'name': product.name,
                'price': str(product.price),
                'qty': quantity
            }

        # Save back to the session and mark it as modified
        request.session['cart'] = cart
        request.session.modified = True

        # Calculate the total quantity in the cart
        total_quantity = sum(item['qty'] for item in cart.values())
        messages.success(request,("Product added to cart"))
        return JsonResponse({'cart_quantity': total_quantity, 'product_qty': cart[product_id]['qty']})
        

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def place_order(request):
    # Get the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    # If the cart has items, create an order
    if cart.items.exists():
        # Create the order
        order = Order.objects.create(user=request.user, cart=cart)

        # Optionally, you can move the cart items to an OrderItem model if needed

        # Clear the cart after placing the order
        cart.items.all().delete()  # Remove all cart items
        cart.delete()  # Optionally delete the cart itself

        # Display success message using Django messages framework
        messages.success(request, 'Your order has been placed successfully!')

        return redirect('home')  # Redirect to the home page or anywhere else you'd like
    else:
        # If there are no items in the cart, redirect to the cart page
        messages.error(request, 'Your cart is empty. Please add items to the cart before placing an order.')
        return redirect('cart_summary')