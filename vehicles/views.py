from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q

from .models import Vehicle
from .forms import VehicleForm


def vehicle_list(request):
    """List all vehicles."""
    vehicles = Vehicle.objects.select_related('purchase_location').all()

    search_query = request.GET.get('search', '').strip()
    if search_query:
        vehicles = vehicles.filter(
            Q(name__icontains=search_query) |
            Q(make__icontains=search_query) |
            Q(model__icontains=search_query) |
            Q(vin__icontains=search_query) |
            Q(license_plate__icontains=search_query) |
            Q(purchase_location__name__icontains=search_query)
        ).distinct()

    return render(request, 'vehicles/list.html', {'object_list': vehicles})


def vehicle_detail(request, pk):
    """Show vehicle details."""
    vehicle = get_object_or_404(Vehicle.objects.select_related('purchase_location'), pk=pk)
    return render(request, 'vehicles/detail.html', {'object': vehicle})


def vehicle_create(request):
    """Create a new vehicle."""
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.save()
            messages.success(request, f'Vehicle "{vehicle.name}" created successfully.')
            if 'save_and_add_another' in request.POST:
                return redirect('vehicles:vehicle_create')
            else:
                return redirect('vehicles:vehicle_detail', pk=vehicle.pk)
    else:
        form = VehicleForm()

    return render(request, 'vehicles/form.html', {'form': form, 'object': None})


def vehicle_update(request, pk):
    """Update an existing vehicle."""
    vehicle = get_object_or_404(Vehicle, pk=pk)

    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            vehicle = form.save()
            messages.success(request, f'Vehicle "{vehicle.name}" updated successfully.')
            return redirect('vehicles:vehicle_detail', pk=vehicle.pk)
    else:
        form = VehicleForm(instance=vehicle)

    return render(request, 'vehicles/form.html', {
        'form': form,
        'object': vehicle
    })


def vehicle_delete(request, pk):
    """Delete a vehicle."""
    vehicle = get_object_or_404(Vehicle, pk=pk)

    if request.method == 'POST':
        vehicle_name = vehicle.name
        vehicle.delete()
        messages.success(request, f'Vehicle "{vehicle_name}" deleted successfully.')
        return redirect('vehicles:vehicle_list')

    return render(request, 'vehicles/confirm_delete.html', {'object': vehicle})