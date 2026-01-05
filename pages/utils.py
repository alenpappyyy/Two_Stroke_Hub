import time

RATE_LIMIT_SECONDS = 30  # 1 message / 30 seconds

def can_send_message(request):
    last = request.session.get("last_contact_time")
    now = time.time()

    if last and now - last < RATE_LIMIT_SECONDS:
        return False

    request.session["last_contact_time"] = now
    return True
