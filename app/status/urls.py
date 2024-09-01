from django.urls import path

from . import views

app_name = "status"

urlpatterns = [
    path("", views.CarStatusView.as_view(), name="home"),
    path("toggle/", views.StatusToggleView.as_view(), name="toggle"),
    path("reservation/", views.ReservationView.as_view(), name="reservation"),
    path(
        "delete_reservation/<int:pk>/",
        views.DeleteReservationView.as_view(),
        name="delete_reservation",
    ),
    path("gasoline/", views.GasolineView.as_view(), name="gasoline"),
]
