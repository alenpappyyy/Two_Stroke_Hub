from django.utils.timezone import now
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from .utils import can_send_message
def home(request):
    return render(request, "pages/home.html")

def about(request):
    return render(request, "pages/about.html")





def contact(request):
    form = ContactForm(request.POST or None)

    if request.method == "POST":
        if not can_send_message(request):
            messages.error(request, "Please wait before sending another message.")
            return redirect("contact")

        if form.is_valid():
            data = form.cleaned_data

            send_mail(
                subject=f"[Contact] {data['subject']}",
                message=data["message"],
                from_email=data["email"],
                recipient_list=["support@twostrokehub.com"],
                fail_silently=True
            )

            messages.success(request, "Message sent successfully 🚀")
            return redirect("contact")

    return render(request, "pages/contact.html", {"form": form})
