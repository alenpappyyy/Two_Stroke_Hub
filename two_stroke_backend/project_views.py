from django.http import JsonResponse
from django.shortcuts import redirect, render
from two_stroke_backend import project_views

def home(request):
    return render(request, "home.html")

def redirect_to_api(request):
    return redirect('/api/')

def homepage_template(request):
    return render(request, 'home.html')


def bikes_store(request):
    return render(request, "bikes/bikes_store.html")
