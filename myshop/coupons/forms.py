from django import forms


class CouponApplyForm(forms.Form):
    """:form:`coupons.CouponApplyForm` is a form allowing users to enter a coupon code.

    Args:
        code (CharField): accepts a coupon code from a user
    """

    code = forms.CharField()
