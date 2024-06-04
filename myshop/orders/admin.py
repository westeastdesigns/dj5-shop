from django.contrib import admin

from .models import Order, OrderItem


# Registers models for order app
class OrderItemInline(admin.TabularInline):
    """OrderItemInline allows :model:`orders.OrderItem` inline in :class:`orders.OrderAdmin`

    This allows the model :model:`orders.OrderItem` to be included on the same edit page
    as its related model :model:`orders.Order`. Its fields are: model (:model:`orders.OrderItem`)
    and raw_id_fields (list)

    Args:
        admin (TabularInline)
    """

    model = OrderItem
    raw_id_fields = ["product"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """OrderAdmin registers :model:`orders.Order` model and includes :model:`orders.OrderItem` inline

    The fields are list_display (list), list_filter (list), and inlines (:class:`orders.OrderItemInline`)

    Args:
        admin (ModelAdmin)
    """

    list_display = [
        "id",
        "first_name",
        "last_name",
        "email",
        "address",
        "postal_code",
        "city",
        "state",
        "paid",
        "created",
        "updated",
    ]
    list_filter = ["paid", "created", "updated"]
    inlines = [OrderItemInline]
