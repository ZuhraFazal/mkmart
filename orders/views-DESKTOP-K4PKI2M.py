from django.shortcuts import render, redirect, get_object_or_404
from cart.models import Cart
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.template.loader import get_template
from cart.cart import Cart
from .models import Order, OrderItem
from products.models import Product


def checkout(request):
    cart = Cart(request)
    cart_items = list(cart)  
    total = cart.get_total_price()

    if request.method == "POST":
        order = Order.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            address=request.POST.get("address"),
            payment_method=request.POST.get("payment"),
            total_price=total,
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                quantity=item["quantity"],
                price=item["product"].price,
            )

        cart.clear()
        return redirect("orders:order_success", order_id=order.id)

    return render(request, "orders/checkout.html", {
        "cart_items": cart_items,
        "total": total,
    })


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = order.items.all()  # order ke items

    return render(request, "orders/order_success.html", {
        "order": order,
        "items": items,
    })


def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        # Direct order create
        order = Order.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            address=request.POST.get("address"),
            payment_method=request.POST.get("payment"),
            total_price=product.price,
        )

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
            price=product.price,
        )

        return redirect("orders:order_success", order_id=order.id)

    return render(request, "orders/buy_now.html", {"product": product})

def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = order.items.all()   # order ke products

    # Response setup
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'

    # Create PDF
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, "Invoice")

    # Customer details
    p.setFont("Helvetica", 12)
    y = height - 100
    p.drawString(50, y, f"Order ID: {order.id}")
    p.drawString(50, y - 20, f"Name: {order.name}")
    p.drawString(50, y - 40, f"Email: {order.email}")
    p.drawString(50, y - 60, f"Phone: {order.phone}")
    p.drawString(50, y - 80, f"Address: {order.address}")

    # Table headers
    y -= 120
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Product")
    p.drawString(250, y, "Qty")
    p.drawString(350, y, "Price")
    p.drawString(450, y, "Subtotal")

    # Items
    y -= 20
    p.setFont("Helvetica", 12)
    for item in items:
        p.drawString(50, y, str(item.product.name))
        p.drawString(250, y, str(item.quantity))
        p.drawString(350, y, f"Rs. {item.price}")
        p.drawString(450, y, f"Rs. {item.price * item.quantity}")
        y -= 20

    # Total
    y -= 20
    p.setFont("Helvetica-Bold", 12)
    p.drawString(350, y, "Total:")
    p.drawString(450, y, f"Rs. {order.total_price}")

    # Save PDF
    p.showPage()
    p.save()

    return response