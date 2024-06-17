from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import views

app_name = "payment"

urlpatterns = [
    # displays order summary, creates Stripe checkout, redirects to Stripe payment form
    path(_("process/"), views.payment_process, name="process"),
    # view for Stripe to redirect user if payment is successful
    path(_("completed/"), views.payment_completed, name="completed"),
    # view for Stripe to redirect user if payment is canceled
    path(_("canceled/"), views.payment_canceled, name="canceled"),
]
