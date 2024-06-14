"""
URL configuration for myshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Django admin documentation
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    # Django admin
    path("admin/", admin.site.urls),
    # urls for shopping cart
    path("cart/", include("cart.urls", namespace="cart")),
    # urls for creating an order
    path("orders/", include("orders.urls", namespace="orders")),
    # urls for processing payment of an order
    path("payment/", include("payment.urls", namespace="payment")),
    # urls for managing coupons
    path("coupons/", include("coupons.urls", namespace="coupons")),
    # urls for shop app under custom namespace shop
    path("", include("shop.urls", namespace="shop")),
]

# for serving uploaded media files using the development server
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
