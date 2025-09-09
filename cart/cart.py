from decimal import Decimal
from products.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def increase(self, product):
        """Increase product quantity by 1"""
        self.add(product, 1)

    def decrease(self, product):
        """Decrease product quantity by 1, remove if qty = 0"""
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] -= 1
            if self.cart[product_id]['quantity'] <= 0:
                self.remove(product)
            else:
                self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        self.session['cart'] = {}
        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            cart_item = self.cart[str(product.id)].copy()
            cart_item['product'] = product
            cart_item['quantity'] = int(cart_item['quantity'])
            cart_item['total_price'] = Decimal(cart_item['price']) * cart_item['quantity']
            yield cart_item

    def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )
