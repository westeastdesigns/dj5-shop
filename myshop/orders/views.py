from cart.cart import Cart
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import OrderCreateForm
from .models import Order, OrderItem
from .tasks import order_created


# views for orders app
def order_create(request):
    """order_create view handles :form:`orders.OrderCreateForm` and creates a new order.

    Args:
        request (GET): instantiates the :form:`orders.OrderCreateForm` and renders the
            :template:`orders/order/create.html` template.
        request (POST): validates the data sent in the request. If valid, a new order is
            created in the database. Cart items are iterated over and for each item an
            :model:`orders.OrderItem` model is created. Then the contents of the cart
            are cleared and the :template:`orders/order/created.html` is rendered.

    Returns:
        HttpResponse: displays create.html or created.html depending on request type.

    """
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            # clear the cart
            cart.clear()
            # launch asynchronous task with Celery
            order_created.delay(order.id)
            # set the order in the session
            request.session["order_id"] = order.id
            # redirect for payment
            return redirect("payment:process")
    else:
        form = OrderCreateForm()
    return render(request, "orders/order/create.html", {"cart": cart, "form": form})


# custom admin view displays info about an order
@staff_member_required
def admin_order_detail(request, order_id):
    """admin_order_detail custom admin view displays info to staff about an order.

    Args:
        request
        order_id (int): unique identifier for an order

    Returns:
        HttpRequest: details about the queried order
    """
    order = get_object_or_404(Order, id=order_id)
    return render(request, "admin/orders/order/detail.html", {"order": order})
