from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from timer.models import CountdownTimer


class CountdownTimerAPITest(TestCase):
    """Test cases for the Countdown Timer API"""

    def setUp(self):
        """Setup test client and data"""
        self.client = APIClient()
        self.timer_data = {
            "event_name": "Test Event",
            "hours": 0,
            "minutes": 5,
            "seconds": 30
        }
        self.timer = CountdownTimer.objects.create(**self.timer_data)
        self.timer_url = f"/api/timers/{self.timer.id}/"

    def test_create_timer(self):
        """Test API can create a countdown timer"""
        response = self.client.post("/api/timers/", self.timer_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["event_name"], "Test Event")

    def test_get_timer(self):
        """Test API can retrieve a countdown timer"""
        response = self.client.get(self.timer_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["event_name"], self.timer.event_name)

    def test_update_timer(self):
        """Test API can update an existing countdown timer"""
        updated_data = {
            "event_name": "Updated Event",
            "hours": 1,
            "minutes": 10,
            "seconds": 0
        }
        response = self.client.put(self.timer_url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["event_name"], "Updated Event")

    def test_delete_timer(self):
        """Test API can delete a countdown timer"""
        response = self.client.delete(self.timer_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CountdownTimer.objects.filter(id=self.timer.id).exists())
