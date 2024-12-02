from django.urls import include, path
from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)
router.register(r"categories", views.CategoryViewSet)
router.register(r"products", views.ProductsViewSet)
# router.register(r"reviews", views.ReviewViewSet, basename="reviews")


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path(
        "products-by-category-api/<int:category_id>/",
        views.ProductListByCategoryViewSet.as_view(),
        name="products-by-category-api",
    ),
    path(
        "products/<int:product_id>/reviews-get",
        views.ReviewViewSet.as_view({"get": "list"}),
        name="products-reviews",
    ),
    path(
        "products/<int:product_id>/reviews-post",
        views.ReviewViewSet.as_view({"get": "post"}),
        name="products-reviews",
    ),
]
