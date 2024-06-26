from django import forms
from django.utils.translation import gettext_lazy as _

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    """CartAddProductForm is a form to add products to the cart.

    Args:
        forms quantity (TypedChoiceField): integer representing the quantity, between 1 and 20.

    """

    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label=_("Quantity")
    )
    override = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput
    )
