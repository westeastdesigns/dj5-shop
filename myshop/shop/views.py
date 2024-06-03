from django.shortcuts import get_object_or_404, render

from .models import Category, Product


# Views for the shop application
def product_list(request, category_slug=None):
    """product_list View lists all the products or filters products by a given category.

    Args:
        request (object): Category, Product to query
        category_slug (SlugField, optional): url-friendly representation of category.
            Defaults to None. Allows filtering by a category, using its slug

    Returns:
        HttpResponse: lists the available products filtered by category
    """
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(
        request,
        "shop/product/list.html",
        {"category": category, "categories": categories, "products": products},
    )


def product_detail(request, id, slug):
    """product_detail retrieves and displays a single product, using its id and slug.

    Args:
        request
        id (int): unique identifier for the product
        slug (SlugField): url-friendly title of the product

    Returns:
        HttpResponse: displays the details about a single product
    """
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request, "shop/product/detail.html", {"product": product})
