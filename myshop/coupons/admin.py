from django.contrib import admin

from .models import Coupon


# Registers models for the coupons app
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    """CouponAdmin registers the :model:`coupons.Coupon` model on the admin site.

    Args:
        list_display (list of strings): displays code, valid_from, valid_to, discount, and active
        list_filter (list of strings): allows filtering by active, valid_from, and valid_to
        search_fields (list of strings): allows searching through the coupon codes

    """

    list_display = [
        "code",
        "valid_from",
        "valid_to",
        "discount",
        "active",
    ]
    list_filter = ["active", "valid_from", "valid_to"]
    search_fields = ["code"]
