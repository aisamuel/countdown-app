from django.test import TestCase
from timer.models import CountdownTimer


class CountdownTimerModelTest(TestCase):
    """Tests for the CountdownTimer model"""

    def test_create_timer(self):
        """Test creating a timer instance"""
        timer = CountdownTimer.objects.create(
            event_name="Model Test",
            hours=1,
            minutes=20,
            seconds=10
        )
        self.assertEqual(str(timer), "Model Test (1h 20m 10s)")
        self.assertEqual(timer.total_seconds(), 4810)
