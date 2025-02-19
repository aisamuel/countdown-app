from django.db import models

class CountdownTimer(models.Model):
    event_name = models.CharField(max_length=255)
    hours = models.PositiveIntegerField(default=0)
    minutes = models.PositiveIntegerField(default=0)
    seconds = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_seconds(self):
        return self.hours * 3600 + self.minutes * 60 + self.seconds

    def __str__(self):
        return f"{self.event_name} ({self.hours}h {self.minutes}m {self.seconds}s)"

