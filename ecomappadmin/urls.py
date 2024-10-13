
from django.urls import include, path
from .views import *
app_name = "ecomappadmin"
urlpatterns = [
    path("admin-home/", AdminHomeView.as_view(), name="admin-home"),
    path("admin-login/", AdminLoginView.as_view(), name="admin-login"),
    path("admin-orders-received/", AdminOrderReceivedView.as_view(), name="admin-orders-received"),
    path("admin-orders-processing/", AdminOrderProcessingView.as_view(), name="admin-orders-processing"),
    path("admin-orders-completed/", AdminOrderCompletedView.as_view(), name="admin-orders-completed"),
    path("admin-orders-way/", AdminOrderWayView.as_view(), name="admin-orders-way"),
    path("admin-orders-canceled/", AdminOrderCanceledView.as_view(), name="admin-orders-canceled"),
    path("admin-order-detail/<int:pk>/", AdminOrderDetailView.as_view(), name="admin-order-detail"),
    path("admin-order-change-status-<int:pk>", AdminOrderStatusChangeView.as_view(), name="admin-order-change-status"),
    path("add-product/", ProductAddView.as_view(), name="add-product"),
    path("product-list", ProductListView.as_view(), name="product-list"),
    path("product-detail/<slug:slug>/", ProductDetailView.as_view(), name="admin-product-detail")
]

