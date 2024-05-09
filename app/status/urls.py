from django.urls import path

from . import views

urlpatterns = [
    path('', views.CarStatusAPIView.as_view(), name='status'),
]
