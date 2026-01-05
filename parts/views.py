from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.viewsets import ModelViewSet

from .models import Part
from .serializers import PartSerializer
from .forms import PartForm


#

def parts_store(request):
    parts = Part.objects.all().order_by('-created_at')
    return render(request, "parts/parts_store.html", {"parts": parts})


def parts_list(request):
    parts = Part.objects.all().order_by('-created_at')
    return render(request, "parts/parts_list.html", {"parts": parts})


def part_detail(request, pk):
    part = get_object_or_404(Part, pk=pk)
    return render(request, "parts/part_detail.html", {"part": part})


def add_part(request):
    if request.method == "POST":
        form = PartForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("parts_list")
    else:
        form = PartForm()

    return render(request, "parts/add_part.html", {"form": form})



class PartViewSet(ModelViewSet):
    queryset = Part.objects.all().order_by('-created_at')
    serializer_class = PartSerializer
