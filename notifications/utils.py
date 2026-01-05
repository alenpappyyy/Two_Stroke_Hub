from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification

def notify(user, message):
    notification = Notification.objects.create(
        user=user,
        message=message
    )

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user.id}",
        {
            "type": "send_notification",
            "id": notification.id,
            "message": message,
        }
    )


def notify_user(user, message):
    # 🗃 Save to DB
    notification = Notification.objects.create(
        user=user,
        message=message
    )

    # ⚡ Send via WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user.id}",
        {
            "type": "send_notification",
            "message": notification.message,
            "id": notification.id,
            "created_at": notification.created_at.isoformat(),
        }
    )