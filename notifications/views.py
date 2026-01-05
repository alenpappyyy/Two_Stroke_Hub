from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Notification
from django.shortcuts import render

@login_required
def mark_read(request, pk):
    notification = get_object_or_404(
        Notification, pk=pk, user=request.user
    )
    notification.is_read = True
    notification.save()
    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def mark_all_read(request):
    request.user.notifications.update(is_read=True)
    return redirect(request.META.get("HTTP_REFERER", "/"))



@login_required
def notification_list(request):
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "notifications/notification_list.html",
        {
            "notifications": notifications
        }
    )
