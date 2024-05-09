from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Status
from .serializers import StatusSerializer

class CarStatusAPIView(APIView):
    def get(self, request):
        serializer = StatusSerializer(Status.objects.first())
        return Response(serializer.data, headers={'Access-Control-Allow-Origin': '*'})
    def post(self, request):
        # statusを切り替える
        status = Status.objects.first()
        status.is_using = not status.is_using
        status.save()
        serializer = StatusSerializer(status)
        return Response(serializer.data, headers={'Access-Control-Allow-Origin': '*'})
