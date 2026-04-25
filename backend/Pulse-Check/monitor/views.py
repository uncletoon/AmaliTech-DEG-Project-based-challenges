from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Monitor
from .serializers import MonitorSerializer

class MonitorViewSet(viewsets.ModelViewSet):
    queryset = Monitor.objects.all()
    serializer_class = MonitorSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        monitor = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def heartbeat(self, request, pk=None):
        try:
            monitor = self.get_object()
        except Monitor.DoesNotExist:
            return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
        monitor.status = 'active'
        monitor.last_heartbeat = timezone.now()
        monitor.save()
        
        return Response({"message": "Heartbeat received"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def pause(self, request, pk=None):
        monitor = self.get_object()
                
        monitor.status = 'paused'
        monitor.save()
        
        return Response({"message": "Monitor paused"}, status=status.HTTP_200_OK)
