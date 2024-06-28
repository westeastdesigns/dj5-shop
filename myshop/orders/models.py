from decimal import Decimal

from coupons.models import Coupon
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    """:model:`orders.Order` stores data about order details.

    Args:
        first_name (CharField): first name of customer
        last_name (CharField): last name of customer
        email (EmailField): email address of customer
        address (CharField): mailing address of customer
        postal_code (CharField): zip code of customer
        city (CharField): city of customer
        created (DateTimeField): when the order was created
        updated (DateTimeField): when the order was most recently updated
        paid (BooleanField): whether the order has been paid for or not, false by default
        stripe_id (CharField): unique id of a Stripe payment associated with this order

    Returns:
        string: order and id of order
        int: total cost of order

    """

    first_name = models.CharField(_("first name"), max_length=50)
    last_name = models.CharField(_("last name"), max_length=50)
    email = models.EmailField(_("e-mail"))
    address = models.CharField(_("address"), max_length=250)
    postal_code = models.CharField(_("postal_code"), max_length=20)
    city = models.CharField(_("city"), max_length=100)
    state = models.CharField(_("state"), max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=250, blank=True)
    coupon = models.ForeignKey(
        Coupon,
        related_name="orders",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    discount = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
        ]

    def __str__(self) -> str:
        return f"Order {self.id}"  # type: ignore

    def get_total_weight(self) -> int:
        """get_total_weight finds the total weight of all products in the order.

        For each item in the order, this method computes the weight of each product by
        multiplying its weight by how many of that product is being ordered. After all
        items in the order have weights calculated, all the weights are added together
        and that sum is returned as an integer. Weights are stored in grams as a
        PositiveIntegerField in the :model:`shop.Product` model.

        Returns:
            integer: weight of all items in the order, calculated in grams

        """
        return sum(item.get_weight() for item in self.items.all())  # type: ignore

    def get_shipping_cost(self) -> Decimal:
        """get_shipping_cost finds the cost of shipping for an order. Three fee tiers.

        Assigns the sum found by the get_total_weight method to the variable total_weight.
        Returns 0.00 if total_weight is zero (indicating there are no physical products),
        otherwise calculates shipping cost based on weight tiers.
        The three weight tiers are calculated by weight as follows:
            (A) if the value is less than or equal to 500 grams, 5.00 is returned.
            (B) Else if the value is less than or equal to 2000 grams, 10.00 is returned.
            (C) Otherwise, assume the value is greater than 2000 grams and 20.00 is returned.

        Returns:
            decimal: Shipping cost based on the total weight of the order.

        """
        total_weight = self.get_total_weight()
        if total_weight == 0:
            return Decimal("0.00")
        elif total_weight <= 500:
            return Decimal("5.00")
        elif total_weight <= 2000:
            return Decimal("10.00")
        else:
            return Decimal("20.00")

    def get_total_cost_before_discount(self) -> Decimal:
        return sum(item.get_cost() for item in self.items.all())  # type: ignore

    def get_discount(self) -> Decimal:
        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return total_cost * (Decimal(self.discount) / Decimal(100))
        return Decimal(0)

    def get_total_cost(self) -> Decimal:
        """get_total_cost gets the total cost of order, including discount and shipping.

        The total cost before the discount is found, then the amount of any discounts
        are removed from the total cost. Then the shipping cost is found and removed.

        Returns:
            integer: This returns the total cost of the order as an integer with 2 decimals.

        """
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount() + self.get_shipping_cost()

    def get_stripe_url(self) -> str:
        """get_stripe_url returns the Stripe dashboard's url for the payment of this order.

        Returns:
            string: url of the Stripe dashboard page associated with the payment of this order

        """
        if not self.stripe_id:
            # no payment associated
            return ""
        if "_test_" in settings.STRIPE_SECRET_KEY:
            # Stripe path for test payments
            path = "/test/"
        else:
            # Stripe path for real payments
            path = "/"
        return f"https://dashboard.stripe.com{path}payments/{self.stripe_id}"


class OrderItem(models.Model):
    """:model:`orders.OrderItem` stores items bought, including price and quantity.

    Args:
        order (ForeignKey): references Order table
        product (ForeignKey): references Product table
        price (DecimalField): price paid for item bought
        quantity (PositiveIntegerField): quantity of item bought
        weight (PositiveIntegerField): weight in grams of item bought

    Returns:
        string: product bought
        int: price x quantity

    """

    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        "shop.Product", related_name="order_items", on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return str(self.id)  # type: ignore

    def get_cost(self) -> Decimal:
        return self.price * Decimal(self.quantity)

    def get_weight(self) -> int:
        """Calculate the total weight of this item."""
        return self.product.weight * self.quantity
