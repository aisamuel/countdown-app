from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CountdownTimerViewSet

router = DefaultRouter()
router.register(r'timers', CountdownTimerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
