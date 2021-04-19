from django.urls import path
from django.conf.urls import include

from . import views

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
    path("redirect_func/<int:_id>", views.redirect_func, name="redirect_func"),
    path("create/", views.create_url, name="create"),
    path("delete_link/<int:id>", views.delete_link, name="delete_link"),
    path("edit_url/<int:id>", views.edit_url, name="edit_url"),
    path("edit_link/<int:id>", views.edit_link, name="edit_link"),
    path("statistics/<str:_id>", views.statistics, name="statistics"),
    path("statistics_ip/<str:ip>", views.statistics_ip, name="statistics_ip"),
]