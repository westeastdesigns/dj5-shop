from cart.forms import CartAddProductForm
from django.shortcuts import get_object_or_404, render

from .models import Category, Product
from .recommender import Recommender


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
        language = request.LANGUAGE_CODE
        category = get_object_or_404(
            Category,
            translations__language_code=language,
            translations__slug=category_slug,
        )
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
    language = request.LANGUAGE_CODE
    product = get_object_or_404(
        Product,
        id=id,
        translations__language_code=language,
        translations__slug=slug,
        available=True,
    )
    cart_product_form = CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    return render(
        request,
        "shop/product/detail.html",
        {
            "product": product,
            "cart_product_form": cart_product_form,
            "recommended_products": recommended_products,
        },
    )
