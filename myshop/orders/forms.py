from django import forms
from localflavor.us.forms import USZipCodeField

from .models import Order


class OrderCreateForm(forms.ModelForm):
    """OrderCreateForm is a form to enter the details of an order.

    This connects to the :view:`cart.order_create` view. postal_code requires a valid US
    zip code to create a new order.

    Args:
        forms (model): :model:`orders.Order`

    """

    postal_code = USZipCodeField()

    class Meta:
        model = Order
        fields = [
            "first_name",
            "last_name",
            "email",
            "address",
            "city",
            "state",
            "postal_code",
        ]
