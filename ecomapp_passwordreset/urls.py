
from django.urls import include, path

app_name = "passreset"
urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
]
