from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .cart import Cart


def view_cart(request):
    cart = Cart(request)
    cart_items = list(cart)
    total = cart.get_total_price()

    return render(request, "cart/view_cart.html", {
        "cart_items": cart_items,
        "total": total,
    })


def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, quantity=1)
    return redirect("cart:view_cart")


def remove_item(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart:view_cart")


def increase_quantity(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.increase(product)
    return redirect("cart:view_cart")


def decrease_quantity(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.decrease(product)
    return redirect("cart:view_cart")
