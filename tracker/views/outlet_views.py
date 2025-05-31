from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
import logging

from tracker.models import Outlet, Room
from tracker.forms import OutletForm

logger = logging.getLogger(__name__)


def outlet_list(request):
    """List all outlets with search and filtering."""
    outlets = Outlet.objects.select_related('room').all()
    return render(request, 'tracker/outlets/list.html', {"object_list": outlets})


def outlet_detail(request, pk):
    """Display outlet details."""
    outlet = get_object_or_404(Outlet.objects.select_related('room'), pk=pk)

    context = {
        'outlet': outlet,
    }

    return render(request, 'tracker/outlets/detail.html', context)


def outlet_create(request):
    """Create a new outlet."""
    if request.method == 'POST':
        form = OutletForm(request.POST)
        if form.is_valid():
            outlet = form.save()
            messages.success(request, f'Outlet in {outlet.room.name} created successfully.')
            return redirect('tracker:outlet_detail', pk=outlet.pk)
    else:
        form = OutletForm()

    return render(request, 'tracker/outlets/form.html', {
        'form': form,
        'outlet': None
    })


def outlet_update(request, pk):
    """Update an existing outlet."""
    outlet = get_object_or_404(Outlet, pk=pk)

    if request.method == 'POST':
        form = OutletForm(request.POST, instance=outlet)
        if form.is_valid():
            outlet = form.save()
            messages.success(request, f'Outlet in {outlet.room.name} updated successfully.')
            return redirect('tracker:outlet_detail', pk=outlet.pk)
    else:
        form = OutletForm(instance=outlet)

    return render(request, 'tracker/outlets/form.html', {
        'form': form,
        'outlet': outlet
    })


def outlet_delete(request, pk):
    """Delete an outlet."""
    outlet = get_object_or_404(Outlet, pk=pk)

    if request.method == 'POST':
        outlet_info = f"{outlet.get_device_type_display()} in {outlet.room.name}"
        outlet.delete()
        messages.success(request, f'Outlet "{outlet_info}" deleted successfully.')
        return redirect('tracker:outlet_list')

    return render(request, 'tracker/outlets/confirm_delete.html', {
        'outlet': outlet
    })
