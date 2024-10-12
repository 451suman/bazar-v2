
from django.urls import include, path
from .views import *
app_name = "ecomappadmin"
urlpatterns = [
    path("admin-home/", AdminHomeView.as_view(), name="admin-home"),
    path("admin-login/", AdminLoginView.as_view(), name="admin-login"),

]

