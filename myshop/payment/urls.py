from django.urls import path

from . import views

app_name = "payment"

urlpatterns = [
    # displays order summary, creates Stripe checkout, redirects to Stripe payment form
    path("process/", views.payment_process, name="process"),
    # view for Stripe to redirect user if payment is successful
    path("completed/", views.payment_completed, name="completed"),
    # view for Stripe to redirect user if payment is canceled
    path("canceled/", views.payment_canceled, name="canceled"),
]
