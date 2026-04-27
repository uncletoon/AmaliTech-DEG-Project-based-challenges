from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Monitor
from .serializers import MonitorSerializer
from .services.monitor_services import (
    create_monitor,
    handle_heartbeat,
    pause_monitor,
)


class MonitorViewSet(viewsets.ModelViewSet):
    queryset = Monitor.objects.all()
    serializer_class = MonitorSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        monitor = create_monitor(serializer.validated_data)

        return Response(
            self.get_serializer(monitor).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["post"])
    def heartbeat(self, request, pk=None):
        get_object_or_404(Monitor, id=pk)

        monitor = handle_heartbeat(pk)

        return Response(
            {
                "message": "Heartbeat received",
                "monitor": self.get_serializer(monitor).data,
            },
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"])
    def pause(self, request, pk=None):
        get_object_or_404(Monitor, id=pk)

        monitor = pause_monitor(pk)

        return Response(
            {
                "message": "Monitor paused",
                "monitor": self.get_serializer(monitor).data,
            },
            status=status.HTTP_200_OK
        )