from rest_framework import viewsets
from .models import CountdownTimer
from .serializers import CountdownTimerSerializer

class CountdownTimerViewSet(viewsets.ModelViewSet):
    queryset = CountdownTimer.objects.all()
    serializer_class = CountdownTimerSerializer
