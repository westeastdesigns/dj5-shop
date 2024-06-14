from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .forms import CouponApplyForm
from .models import Coupon


# View for coupon entry form
@require_POST
def coupon_apply(request):
    """:view:`coupons.coupon_apply` view validates the coupon + stores it in user's session.

    :form:`coupons.CouponApplyForm` is instantiated using the posted data, + checks that
    the form is valid.
    If valid, gets the code entered by user from the form's cleaned_data dictionary.
    Tries to retrieve the Coupon object with the given code. Uses iexact lookup to perform
    a case-sensitive match. Coupon must be currently active and valid for current datetime.
    The coupon ID is stored in the user's session.
    The user is redirected to the cart_detail url, displaying cart with coupon applied.

    Args:
        request (POST): only a POST request is allowed

    Returns:
        HttpResponse: redirects to cart_detail url, displaying cart with coupon applied.

    """
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data["code"]
        try:
            coupon = Coupon.objects.get(
                code__iexact=code,
                valid_from__lte=now,
                valid_to__gte=now,
                active=True,
            )
            request.session["coupon_id"] = coupon.id
        except Coupon.DoesNotExist:
            request.session["coupon_id"] = None
    return redirect("cart:cart_detail")
