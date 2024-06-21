import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Order, OrderItem


def export_to_csv(modeladmin, request, queryset):
    """export_to_csv is a custom admin action to download a list of orders as a csv file.

    Args:
        modeladmin (class): current :class:`admin.ModelAdmin` being displayed
        request (object): current request object as an HttpRequest instance
        queryset (QuerySet): a QuerySet for the objects selected by the user

    Returns:
        HttpResponse: contains an attached csv file of the requested orders

    """
    opts = modeladmin.model._meta
    content_disposition = f"attachment; filename={opts.verbose_name}.csv"
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = content_disposition
    writer = csv.writer(response)
    fields = [
        field
        for field in opts.get_fields()
        if not field.many_to_many and not field.one_to_many
    ]
    # write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime("%m/%d/%Y")
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = "Export to CSV"


# Registers models for order app
class OrderItemInline(admin.TabularInline):
    """OrderItemInline allows :model:`orders.OrderItem` inline in :class:`orders.OrderAdmin`

    This allows the model :model:`orders.OrderItem` to be included on the same edit page
    as its related model :model:`orders.Order`. Its fields are: model (:model:`orders.OrderItem`)
    and raw_id_fields (list)

    Args:
        model: (:model:`orders.OrderItem`)
        raw_id_fields: (list)

    """

    model = OrderItem
    raw_id_fields = ["product"]


def order_payment(obj):
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)
    return ""


order_payment.short_description = "Stripe payment"


def order_detail(obj):
    """order_detail adds a link to each Order object on the list display page of admin site.

    Args:
        obj (object): Order object

    Returns:
        string: HTML link for the admin_order_detail url. mark_safe prevents auto-escape.

    """
    url = reverse("orders:admin_order_detail", args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')


def order_pdf(obj):
    """order_pdf adds a link to the PDF file for each result.

    Args:
        obj (object): Order object

    Returns:
        string: HTML link for the admin_order_pdf url. mark_safe prevents auto-escape.

    """
    url = reverse("orders:admin_order_pdf", args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')


order_pdf.short_description = "Invoice"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """OrderAdmin registers :model:`orders.Order` model and includes :model:`orders.OrderItem` inline

    The fields are list_display (list), list_filter (list), and inlines (:class:`orders.OrderItemInline`)

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
        order_payment,
        "created",
        "updated",
        order_detail,
        order_pdf,
    ]
    list_filter = ["paid", "created", "updated"]
    inlines = [OrderItemInline]
    actions = [export_to_csv]
