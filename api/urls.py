from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers


router = routers.DefaultRouter()

router.register("products", views.ProductsViewSet)
router.register("categories", views.CategoryViewSet)
router.register("carts", views.CartViewSet)
router.register("n_profiles", views.ProfileViewSet)
router.register("orders", views.OrderViewSet, basename="orders")


product_router = routers.NestedDefaultRouter(router, "products", lookup="product")
product_router.register("reviews", views.ReviewViewSet, basename="product-reviews")


cart_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")
cart_router.register("items", views.CartItemViewSet, basename="cart-items")



urlpatterns = [
    path("", include(router.urls)),
    path("", include(product_router.urls)),
    path("", include(cart_router.urls))
    # path("products", views.ApiProducts.as_view()),
    # path("products/<str:pk>", views.ApiProduct.as_view()),
    # path("categories", views.APICategories.as_view()),
    # path("categories/<str:pk>", views.APICategory.as_view())
]