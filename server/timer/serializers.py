from rest_framework import serializers
from .models import CountdownTimer

class CountdownTimerSerializer(serializers.ModelSerializer):
    total_seconds = serializers.ReadOnlyField()

    class Meta:
        model = CountdownTimer
        fields = ['id', 'event_name', 'hours', 'minutes', 'seconds', 'total_seconds']
