from django.urls import include, path
from .views import *
from django.contrib.auth import views as auth_views
app_name = "ecomapp"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    
    path('change-password/', auth_views.PasswordChangeView.as_view(), name='change-password'),
    path('change-password/done/', auth_views.PasswordChangeDoneView.as_view(), name='change-password-done'),

    path("products/", ProductListView.as_view(), name="products"),
    # path("product/<int:pk>/", idProductDetailView.as_view(), name="productdetail"),
    path("product/<slug:slug>/", ProductDetailView.as_view(), name="productdetail"),
    path("submit-review/<slug:slug>/", ReviewSubmit.as_view(), name="reviewsubmit"),

    # product select buy category id
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

    path("my-account/", CustomerProfileView.as_view(), name="customerprofile"),
    path("profile/order-<int:pk>/", CustomerOrderDetailView.as_view(), name = "customerorderdetail"),
    path("change-profile-detail-change", CustomerDetailChange.as_view(), name = "customerdetailchange"),
    path("contact/", ContactView.as_view(), name="contact"),
]
