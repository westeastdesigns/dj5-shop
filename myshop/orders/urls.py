from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    # url pattern for the :view:`orders.OrderCreate` view
    path("create/", views.order_create, name="order_create"),
    # view for staff to view details of an order
    path(
        "admin/order/<int:order_id>",
        views.admin_order_detail,
        name="admin_order_detail",
    ),
    # view for creating a pdf invoice of an order
    path(
        "admin/order/<int:order_id>/pdf/",
        views.admin_order_pdf,
        name="admin_order_pdf",
    ),
]
