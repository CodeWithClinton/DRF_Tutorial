from django.urls import path
from . import views

urlpatterns = [
    path("products", views.api_products),
    path("products/<str:pk>", views.api_product),
    path("categories", views.api_categories),
    path("categories/<str:pk>", views.api_category)
]