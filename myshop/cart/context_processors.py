from .cart import Cart


def cart(request):
    """cart context processor instantiates the cart and makes it available to templates.

    cart is instantiated using the request object and makes it available for the
    templates as a variable named cart.

    Args:
        request (object): used to instantiate the cart

    Returns:
        object: cart
    """
    return {"cart": Cart(request)}
