from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):
    """OrderCreateForm is a form to enter the details of an order.

    This connects to the :view:`cart.order_create` view.

    Args:
        forms (model): :model:`orders.Order`

    """

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
