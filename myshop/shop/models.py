from audioop import reverse

from django.db import models


# Defines the tables of data for the shop app
class Category(models.Model):
    """Category model stores a name and slug for the categories of Product.

    :model:`shop.Category` stores data about the categories of :model:`shop.Product`.
    It includes a name field and unique slug field.

    Args:
        name (CharField): String representing category name
        slug (SlugField): String of url-friendly name

    Returns:
        string: name of category
    """

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product_list_by_category", args=[self.slug])


class Product(models.Model):
    """Product model stores data about the items or products in the shop app.

    Products are indexed by id and slug fields together to optimize queries utilizing
    both fields. Products are also indexed by name. There is another index for the created
    field, which is defined in descending order of creation date and time.

    Args:
        category (ForeignKey): connects :model:`shop.Category` to :model:`shop.Product`.
            One-to-Many relationship, product belongs in 1 category, category has many products
        name (CharField): name of product
        slug (SlugField): url-friendly title for the product
        image (ImageField): product image is optional, but encouraged
        description (TextField): product details are optional, but encouraged
        price (DecimalField): decimal.Decimal type stores a fixed-precision decimal number
            with 10 digits at max and two decimal places
        available (BooleanField): indicates whether the product is available
        created (DateTimeField): stores when the object was created
        updated (DateTimeField): stores when the object was last updated

    Returns:
        string: returns the name of the product
    """

    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["id", "slug"]),
            models.Index(fields=["name"]),
            models.Index(fields=["-created"]),
        ]

    def __str__(self):
        return self.name
