from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product, Category
from django.shortcuts import render

def home(request):
    return HttpResponse("Welcome to Mk Mart Home Page")

def about(request):
    return render(request, 'products/about.html')

def product_list(request):
    products = Product.objects.all()
    category_id = request.GET.get('category')
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()

    categories = Category.objects.all()
    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories
    })
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "products/product_detail.html", {"product": product})
