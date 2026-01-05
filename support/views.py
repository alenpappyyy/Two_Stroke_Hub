from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .models import SupportTicket
from .forms import SupportTicketForm

@login_required
def support_home(request):
    return render(request, 'support/support_home.html')

@login_required
def support_list(request):
    tickets = SupportTicket.objects.filter(user=request.user)
    return render(request, 'support/support_list.html', {'tickets': tickets})

@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(
        SupportTicket,
        pk=pk,
        user=request.user
    )
    return render(request, 'support/ticket_detail.html', {'ticket': ticket})

@login_required
def create_ticket(request):
    if request.method == "POST":
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('support:list')
    else:
        form = SupportTicketForm()

    return render(request, 'support/create_ticket.html', {'form': form})
@staff_member_required
def admin_dashboard(request):
    tickets = SupportTicket.objects.all()
    return render(request, 'support/admin_dashboard.html', {'tickets': tickets})

@staff_member_required
def admin_ticket_detail(request, pk):
    ticket = get_object_or_404(SupportTicket, pk=pk)
    return render(request, 'support/admin_ticket_detail.html', {'ticket': ticket})
