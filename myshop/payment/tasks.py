import logging
from io import BytesIO

import weasyprint
from celery import shared_task
from django.contrib.staticfiles import finders
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from orders.models import Order

logger = logging.getLogger(__name__)


@shared_task
def payment_completed(order_id):
    """payment_completed task sends an email notification when an order is successfully paid.

    Args:
        order_id (int): unique identifier for an order

    """
    logger.info(f"Executing payment_completed task for order id: {order_id}")
    try:
        order = Order.objects.get(id=order_id)
        logger.info(f"Order found: {order}")
        # create invoice email
        subject = f"West East Designs Shop - Invoice number {order.id}"
        message = "Thank you for your recent purchase. Your invoice is attached to this email."
        email = EmailMessage(subject, message, "admin@myshop.com", [order.email])
        # generate PDF
        html = render_to_string("orders/order/pdf.html", {"order": order})
        out = BytesIO()
        stylesheets = [weasyprint.CSS(finders.find("css/pdf.css"))]
        weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
        # attach PDF file
        email.attach(f"order_{order.id}.pdf", out.getvalue(), "application/pdf")
        # send email
        email.send()
        logger.info("Email sent successfully")
    except Order.DoesNotExist:
        logger.error(f"Order with id {order_id} does not exist")
    except Exception as e:
        logger.error(f"Error in payment_completed task: {e}")
        raise
