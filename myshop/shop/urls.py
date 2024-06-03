from django.urls import path

from . import views

app_name = "shop"

# url patterns for the product catalog in the shop app
urlpatterns = [
    # view product list without any parameters
    path("", views.product_list, name="product_list"),
    # view product list filtered by a given category
    path("<slug:category_slug>/", views.product_list, name="product_list_by_category"),
    # view details about a single product using its id and slug to retrieve it
    path("<int:id>/<slug:slug>/", views.product_detail, name="product_detail"),
]
