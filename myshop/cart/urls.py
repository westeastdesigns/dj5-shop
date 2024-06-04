"""adds urls for cart views
    :view:`cart.cart_detail`
    :view:`cart.cart_add`
and :view:`cart.cart_remove`

"""

from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    # adds url for cart view :view:`cart.cart_detail`
    path("", views.cart_detail, name="cart_detail"),
    # adds url for cart view :view:`cart.cart_add`
    path("add/<int:product_id>/", views.cart_add, name="cart_add"),
    # adds url for cart view :view:`cart.cart_remove`
    path("remove/<int:product_id>/", views.cart_remove, name="cart_remove"),
]
