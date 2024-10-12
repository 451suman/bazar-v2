
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

]

