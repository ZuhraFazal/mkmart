from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("success/<int:order_id>/", views.order_success, name="order_success"),
    path("invoice/<int:order_id>/", views.download_invoice, name="download_invoice"),  
     path('buy/<int:product_id>/', views.buy_now, name="buy_now"),
]   
