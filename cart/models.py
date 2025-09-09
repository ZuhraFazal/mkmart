from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.shortcuts import redirect, get_object_or_404


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Cart"

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

    @property
    def subtotal(self):
        return self.product.price * self.quantity


def remove_item(request, item_id):
    item = get_object_or_404(Cart, id=item_id)
    item.delete()
    return redirect("cart:cart_view")