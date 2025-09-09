from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from products import views
from django.conf.urls.static import static
from django.shortcuts import render


# home view yahan hi bana sakte ho
def home(request):
    return render(request, "home.html")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'), 
    path('about/', views.about, name='about'),
    path('products/', include('products.urls')),
    path('cart/', include("cart.urls")),
     path("orders/", include("orders.urls")),
    path("contact/", include("contact.urls", namespace="contact")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("accounts.urls")),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
