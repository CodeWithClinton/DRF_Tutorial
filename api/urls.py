from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers


router = routers.DefaultRouter()

router.register("products", views.ProductsViewSet)
router.register("categories", views.CategoryViewSet)
router.register("carts", views.CartViewSet)


product_router = routers.NestedDefaultRouter(router, "products", lookup="product")
product_router.register("reviews", views.ReviewViewSet, basename="product-reviews")




urlpatterns = [
    path("", include(router.urls)),
    path("", include(product_router.urls))
    # path("products", views.ApiProducts.as_view()),
    # path("products/<str:pk>", views.ApiProduct.as_view()),
    # path("categories", views.APICategories.as_view()),
    # path("categories/<str:pk>", views.APICategory.as_view())
]