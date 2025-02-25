from django.urls import path

from apps.websocket.socket_scripts.consumers import ChatConsumer

websocket_urls = [
    path("ws/notify/<str:user_id>/", ChatConsumer.as_asgi(), name="notify"),
]
