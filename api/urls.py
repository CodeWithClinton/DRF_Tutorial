from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("products", views.ProductsViewSet)
router.register("categories", views.CategoryViewSet)

urlpatterns = router.urls

urlpatterns = [
    path("", include(router.urls))
    # path("products", views.ApiProducts.as_view()),
    # path("products/<str:pk>", views.ApiProduct.as_view()),
    # path("categories", views.APICategories.as_view()),
    # path("categories/<str:pk>", views.APICategory.as_view())
]