from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import Appliance, Room, Circuit


def home(request: HttpRequest) -> HttpResponse:
    """Home page showing summary of tracked items."""
    context = {
        'appliance_count': Appliance.objects.count(),
        'room_count': Room.objects.count(),
        'circuit_count': Circuit.objects.count(),
    }
    return render(request, 'tracker/home.html', context)
