from django.contrib import admin
from django.urls import include, path

from crypto.views import signup_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("crypto/", include("crypto.urls")),
    path(
        "accounts/", include("django.contrib.auth.urls")
    ),
    path("accounts/signup/", signup_view, name="signup"),
]
