from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    path('', views.support_home, name='home'),
    path('tickets/', views.support_list, name='ticket_list'),
    path('tickets/create/', views.create_ticket, name='create_ticket'),
    path('tickets/<int:pk>/', views.ticket_detail, name='ticket_detail'),

    # admin
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/tickets/<int:pk>/', views.admin_ticket_detail, name='admin_ticket_detail'),
]
