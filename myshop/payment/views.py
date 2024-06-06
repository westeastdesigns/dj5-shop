from decimal import Decimal

import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from orders.models import Order

# Views for the payment app

# create the Strip instance
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def payment_process(request):
    """payment_process creates a checkout session and redirects users to a payment form.

    payment_process creates a Stripe Checkout Session and redirects the client to the
    Stripe-hosted payment form. A checkout session is a programmatic representation of
    what the client sees when they are redirected to the payment form, including the
    products, quantities, currency, and amount to charge.

    Args:
        request (GET): asks for :template:`payment/process.html`

        request (POST): creates a checkout session and redirects user, using the parameters:
            mode, client_reference_id, success_url, cancel_url, and line_items.

    Returns:
        HttpResponse: :template:`payment/process.html` or redirects the user to Stripe.
    """
    order_id = request.session.get("order_id")
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        success_url = request.build_absolute_url(reverse("payment:completed"))
        cancel_url = request.build_absolute_url(reverse("payment:canceled"))
        # Stripe checkout session data
        session_data = {
            "mode": "payment",
            "client_reference_id": order.id,
            "success_url": success_url,
            "cancel_url": cancel_url,
            "line_items": [],
        }
        # add order items to the Stripe checkout session
        for item in order.items.all():
            session_data["line_items"].append(
                {
                    "price_data": {
                        "unit_amount": int(item.price * Decimal("100")),
                        "currency": "usd",
                        "product_data": {
                            "name": item.product.name,
                        },
                    },
                    "quantity": item.quantity,
                }
            )
        # create Stripe checkout session
        session = stripe.checkout.Session.create(**session_data)
        # redirect to Stripe payment form
        return redirect(session.url, code=303)

    else:
        return render(request, "payment/process.html", locals())


def payment_completed(request):
    """payment_completed displays a message for successful payments.

    The user is redirected to this view if the payment is successful.

    Args:
        request

    Returns:
        HttpResponse: :template:`payment/completed.html`
    """
    return render(request, "payment/completed.html")


def payment_canceled(request):
    """payment_canceled displays a message for cancelled payments.

    The user is redirected to this view if the payment is cancelled.

    Args:
        request

    Returns:
        HttpResponse: :template:`payment/canceled.html`
    """
    return render(request, "payment/canceled.html")
