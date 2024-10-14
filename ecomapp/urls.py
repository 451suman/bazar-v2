from django.urls import path
from .views import *

app_name = "ecomapp"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("products/", ProductListView.as_view(), name="products"),
    # path("product/<int:pk>/", idProductDetailView.as_view(), name="productdetail"),
    path("product/<slug:slug>/", ProductDetailView.as_view(), name="productdetail"),

    path("category-list/<int:cid>/", CategoriesListView.as_view(), name="category-list"),
    path("category/", CategoryListView.as_view(), name="category"),

    path("search/", SearchView.as_view(), name="search"),



    path("my-cart/", MyCartView.as_view(), name="mycart"),
    path("add-to-cart-<int:pro_id>/", AddToCartView.as_view(), name="addtocart"),
    path("manage-cart/<int:cp_id>/", ManageCartView.as_view(), name="managecart"),
    path("empyt-cart/", EmpytCartView.as_view(), name="empycart"),

    path("checkout/", CheckoutView.as_view(), name="checkout"),

    path("register/", CustomerRegisterView.as_view(), name="customerregistration"),
    path("logout/", CustomerLogoutView.as_view(), name="customerlogout"),
    path("login/", CustomerLoginView.as_view(), name="customerlogin"),

    path("profile/", CustomerProfileView.as_view(), name="customerprofile"),
   path("profile/order-<int:pk>/", CustomerOrderDetailView.as_view(), name = "customerorderdetail")
]
