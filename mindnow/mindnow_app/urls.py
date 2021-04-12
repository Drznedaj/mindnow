from django.urls import path
from django.conf.urls import include

from . import views

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
    path("redirect_func/<int:id>", views.redirect_func, name="redirect_func"),
]