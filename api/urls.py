from django.urls import path
from . import views

urlpatterns = [
    path("products", views.ApiProducts.as_view()),
    path("products/<str:pk>", views.ApiProduct.as_view()),
    path("categories", views.APICategories.as_view()),
    path("categories/<str:pk>", views.APICategory.as_view())
]