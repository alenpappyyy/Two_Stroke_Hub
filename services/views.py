from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Service, ServiceBooking
from .forms import ServiceBookingForm
from .utils import send_booking_email
from .models import Service, ServiceCategory


def services_list(request, slug=None):
    categories = ServiceCategory.objects.all()
    services = Service.objects.all()

    if slug:
        services = services.filter(category__slug=slug)

    return render(request, 'services/services_list.html', {
        'categories': categories,
        'services': services
    })

def services_home(request):
    return render(request, "services/home.html")


@login_required
def book_service(request, id):
    service = get_object_or_404(Service, id=id)

    if request.method == 'POST':
        form = ServiceBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.service = service
            booking.save()

            # ✅ SEND EMAIL ON BOOKING
            send_booking_email(
                subject="Service Booking Confirmed",
                message=f"""
Hi {request.user.username},

Your booking for "{service.name}" is successful.

📅 Date: {booking.preferred_date}
💰 Price: ₹{service.price}
📌 Status: Pending

We will contact you soon.

– Two Stroke Hub
""",
                user_email=request.user.email
            )

            return redirect('services:booking_success')
    else:
        form = ServiceBookingForm()

    return render(request, 'services/book_service.html', {
        'service': service,
        'form': form
    })


@login_required
def booking_success(request):
    return render(request, 'services/booking_success.html')


@login_required
def my_bookings(request):
    bookings = ServiceBooking.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'services/my_bookings.html', {
        'bookings': bookings
    })


@login_required
def cancel_booking(request, id):
    booking = get_object_or_404(
        ServiceBooking,
        id=id,
        user=request.user
    )

    if booking.status in ['pending', 'confirmed']:
        booking.status = 'cancelled'
        booking.save()

        # ✅ SEND EMAIL ON CANCEL
        send_booking_email(
            subject="Service Booking Cancelled",
            message=f"""
Hi {request.user.username},

Your booking for "{booking.service.name}" has been cancelled.

📅 Date: {booking.preferred_date}

If this was a mistake, you can book again anytime.

– Two Stroke Hub
""",
            user_email=request.user.email
        )

        messages.success(request, "Booking cancelled successfully.")
    else:
        messages.warning(request, "This booking cannot be cancelled.")

    return redirect('services:my_bookings')



def category_services(request, slug):
    category = get_object_or_404(ServiceCategory, slug=slug)
    services = Service.objects.filter(category=category)
    categories = ServiceCategory.objects.all()

    return render(request, "services/services_list.html", {
        "services": services,
        "categories": categories,
        "active_category": category,
    })