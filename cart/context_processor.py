#from . cart import Cart
#def cart(request):
    #return{'cart':Cart(request)}
def cart_quantity(request):
    cart = request.session.get('cart', {})
    total_quantity = sum(item['qty'] for item in cart.values())
    return {'cart_quantity': total_quantity}
