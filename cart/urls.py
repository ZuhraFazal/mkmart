from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("", views.view_cart, name="view_cart"),
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove/<int:product_id>/", views.remove_item, name="remove_item"),
    path("increase/<int:product_id>/", views.increase_quantity, name="increase_quantity"),
    path("decrease/<int:product_id>/", views.decrease_quantity, name="decrease_quantity"),
]
