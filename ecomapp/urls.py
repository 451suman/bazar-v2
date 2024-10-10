
from django.urls import path
from .views import *

app_name = "ecomapp"
urlpatterns = [
    path ("", HomeView.as_view(), name="home"),
    path("products/",ProductListView.as_view(), name="products"),
     path("product/<int:pk>/", ProductDetailView.as_view(), name = "productdetail"),
   


    path("my-cart/", MyCartView.as_view(), name = "mycart"),
    path("add-to-cart-<int:pro_id>/", AddToCartView.as_view(), name = "addtocart"),
    path("manage-cart/<int:cp_id>/", ManageCartView.as_view(), name = "managecart"),
    path("empyt-cart/", EmpytCartView.as_view(), name = "empycart"),

    path("checkout/", CheckoutView.as_view(), name = "checkout"),


   path("register/", CustomerRegisterView.as_view(), name = "customerregistration"),

]
