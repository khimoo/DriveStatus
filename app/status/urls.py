from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('', views.CarStatusAPIView.as_view(), name='status'),
    path('toggle/', views.StatusToggleView.as_view(), name='toggle'),
]
