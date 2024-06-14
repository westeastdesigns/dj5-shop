from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Defines data stored in tables related to coupons
class Coupon(models.Model):
    """:model:`coupons.Coupon` stores data about coupons.

    Args:
        code (CharField): the unique coupon code users must enter to apply the discount
        valid_from (DateTimeField): indicates when the coupon becomes valid
        valid_to (DateTimeField): indicates when the coupon becomes invalid
        discount (IntegerField): discount rate to apply, a percentage between 0 and 100
        active (BooleanField): indicates whether the coupon is active

    Returns:
        CharField: data in code field

    """

    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage value (0 to 100)",
    )
    active = models.BooleanField()

    def __str__(self):
        return self.code
