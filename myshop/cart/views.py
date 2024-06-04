from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from shop.models import Product

from .cart import Cart
from .forms import CartAddProductForm


# Views for the cart app
@require_POST
def cart_add(request, product_id):
    """:view:`cart.cart_add` view adds products to the cart or updates quantities for existing products.

    Args:
        request (POST): only POST requests are allowed
        product_id (key): identifies the product being queried

    Returns:
        HttpResponse: redirects to the cart_detail url to display updated cart contents
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product, quantity=cd["quantity"], override_quantity=cd["override"]
        )
    return redirect("cart:cart_detail")


@require_POST
def cart_remove(request, product_id):
    """:view:`cart.cart_remove` view removes items from cart.

    Args:
        request (POST): this view only accepts POST requests
        product_id (key): identifies the product being queried for removal

    Returns:
        HttpResponse: redirects to the updated cart
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart:cart_detail")


def cart_detail(request):
    """:view:`cart.cart_detail` view displays the cart and its items.

    Args:
        request

    Returns:
        HttpResponse: retrieves the current cart to display it on the detail page
    """
    cart = Cart(request)
    for item in cart:
        item["update_quantity_form"] = CartAddProductForm(
            initial={"quantity": item["quantity"], "override": True}
        )
    return render(request, "cart/detail.html", {"cart": cart})
