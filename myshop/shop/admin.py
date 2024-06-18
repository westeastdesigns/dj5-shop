from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import Category, Product


# Registers catalog models on the administration site
@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    """CategoryAdmin registers the Category model on the administation site.

    Args:
        list_display (list): contains values for category names and slugs.
        prepopulated_fields (dictionary): specifies fields where the value is
            automatically set using the value of other fields. Useful for generating slugs.

    """

    list_display = ["name", "slug"]

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    """ProductAdmin registers the Product model on the administration site.

    Args:
        list_display (list): contains values for product names, slugs, prices,
            availability, creation date/time, and when the product was last updated.
        list_filter (list): allows list to be filtered by availability, creation
            date/time, and when the product was last updated.
        list_editable (list): allows price and availability to be edited from list
            display page of admin site.
        prepopulated_fields (dictionary): specifies fields where the value is
            automatically set using the value of other fields. Useful for generating slugs.

    """

    list_display = ["name", "slug", "price", "available", "created", "updated"]
    list_filter = ["available", "created", "updated"]
    list_editable = ["price", "available"]

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("name",)}
