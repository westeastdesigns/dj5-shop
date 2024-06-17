"""
URL configuration for myshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from payment import webhooks

urlpatterns = i18n_patterns(
    # Django admin documentation
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    # Django admin
    path("admin/", admin.site.urls),
    # urls for shopping cart
    path(_("cart/"), include("cart.urls", namespace="cart")),
    # urls for creating an order
    path(_("orders/"), include("orders.urls", namespace="orders")),
    # urls for processing payment of an order
    path(_("payment/"), include("payment.urls", namespace="payment")),
    # urls for managing coupons
    path(_("coupons/"), include("coupons.urls", namespace="coupons")),
    # urls for Rosetta translation app
    path("rosetta/", include("rosetta.urls")),
    # urls for shop app under custom namespace shop
    path("", include("shop.urls", namespace="shop")),
)

# append the url pattern for Stripe webhook without translation. It is placed outside of
# i18n_patterns() to ensure a single url is maintained for Stripe event notifications.
urlpatterns += [
    path("payment/webhook/", webhooks.stripe_webhook, name="stripe-webhook"),
]
# for serving uploaded media files using the development server
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
