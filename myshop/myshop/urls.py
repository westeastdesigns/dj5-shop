"""
URL configuration for myshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Django admin documentation
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    # Django admin
    path("admin/", admin.site.urls),
    path("", include("shop.urls", namespace="shop")),
]
