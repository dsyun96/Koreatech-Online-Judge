from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('ws/ide', consumers.IdeConsumer),
    path('ws/status', consumers.StatusConsumer),
]
