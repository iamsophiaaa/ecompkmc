from core.models import Product
class Cart():
    def __init__(self,request):

        self.session=request.session
        self.cart = self.session.get('cart', {})
        if 'cart' not in request.session:
            cart=self.session['session_key']={}
            self.cart=cart

    def add(self,product,quantity):
        product_id=str(product.id)
        product_qty=str(quantity)
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id]=int(product_qty)
            self.session.modified=True
    def __len__(self):
        return len(self.cart)
    
    def get_products(self):
        product_id=self.cart.keys()
        products=Product.objects.filter(id__in=product_id)
        return products    
    def get_quants(self):
        quantities=self.cart
        return quantities       
    