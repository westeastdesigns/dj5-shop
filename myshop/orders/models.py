from django.db import models


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

    Returns:
        string: order and id of order
        int: total cost of order
    """

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
        ]

    def __str__(self) -> str:
        return f"Order {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    """:model:`orders.OrderItem` stores items bought, including price and quantity.

    Args:
        order (ForeignKey): references Order table
        product (ForeignKey): references Product table
        price (DecimalField): price paid for item bought
        quantity (PositiveIntegerField): quantity of item bought

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
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
