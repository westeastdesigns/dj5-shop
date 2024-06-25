import logging

import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order
from shop.models import Product
from shop.recommender import Recommender

from .tasks import payment_completed

logger = logging.getLogger(__name__)


@csrf_exempt
def stripe_webhook(request):
    """stripe_webhook verifies with Stripe if the order is complete, then marks it paid.

    The webhook verifies the signature, raises exception if invalid. Then it constructs
    an event from JSON payload, checks for completed checkout session, raises exception
    if the order doesn't exist. If the order is valid and status is paid, order is
    marked as paid in the database.

    Args:
        request

    Returns:
        HttpResponse: redirects according to status of order and response from Stripe

    """
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    logger.info(f"Received event: {event}")

    if event.type == "checkout.session.completed":
        session = event.data.object
        logger.info(f"Session data: {session}")
        if session.mode == "payment" and session.payment_status == "paid":
            try:
                order = Order.objects.get(id=session.client_reference_id)
                logger.info(f"Order found: {order}")
            except Order.DoesNotExist:
                logger.error("Order does not exist")
                return HttpResponse(status=404)
            # mark order as paid
            order.paid = True
            # store Stripe payment ID
            order.stripe_id = session.payment_intent
            order.save()

            # save items bought for product recommendations
            product_ids = order.items.values_list("product_id")
            products = Product.objects.filter(id__in=product_ids)
            r = Recommender()
            r.products_bought(products)

            # launch asynchronous task
            payment_completed.delay(order.id)
            logger.info("Launched payment_completed task")

    return HttpResponse(status=200)
