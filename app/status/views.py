from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import View, TemplateView
from django.shortcuts import render
from django.shortcuts import redirect

from .models import Status
from .serializers import StatusSerializer


class CarStatusAPIView(TemplateView):

    template_name = 'base.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['is_using'] = Status.objects.first().is_using
        return context

class StatusToggleView(View):
    def get(self, request, *args, **kwargs):
        status = Status.objects.first()
        status.is_using = not status.is_using
        status.save()
        return redirect('api:status')
