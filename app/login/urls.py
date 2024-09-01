from django.urls import path

from . import views

app_name = "login"

urlpatterns = [
    path("", views.LoginView.as_view(), name="login"),
]
