from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.crypto_request_view, name="crypto_request"),
]

urlpatterns += [
    path("about/", views.crypto_about_view, name="crypto_about"),
]


urlpatterns += [
    path("signup/", views.signup_view, name="signup"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]


urlpatterns += [
    path("graph/", views.crypto_graph_view, name="crypto_graph"),
]
