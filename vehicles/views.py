from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.urls import reverse
from vehicles.models import Vehicle, MaintenanceRecord
from vehicles.forms import VehicleForm, MaintenanceRecordForm


def list(request: HttpRequest) -> HttpResponse:
    """List all vehicles."""
    vehicles = Vehicle.objects.all()
    vehicles_needing_service = Vehicle.objects.filter(
        current_mileage__isnull=False,
        last_oil_change_mileage__isnull=False
    ).extra(
        where=["current_mileage - last_oil_change_mileage >= 5000"]
    )
    context = {
        'vehicles': vehicles,
        'vehicles_needing_service': vehicles_needing_service,
    }
    return render(request, 'vehicles/index.html', context)


def detail(request: HttpRequest, pk: int) -> HttpResponse:
    """Show details for a specific vehicle."""
    vehicle = get_object_or_404(Vehicle, pk=pk)
    recent_maintenance = vehicle.maintenance_records.all()[:5]
    context = {
        'vehicle': vehicle,
        'recent_maintenance': recent_maintenance,
    }
    return render(request, 'vehicles/detail.html', context)


def create(request: HttpRequest) -> HttpResponse:
    """Create a new vehicle."""
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.save()
            messages.success(request, f'Vehicle {vehicle} created successfully.')
            return redirect('vehicles:detail', pk=vehicle.pk)
    else:
        form = VehicleForm()
    context = {
        'form': form,
        'title': 'Add New Vehicle',
    }
    return render(request, 'vehicles/form.html', context)


def update(request: HttpRequest, pk: int) -> HttpResponse:
    """Update an existing vehicle."""
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            vehicle = form.save()
            messages.success(request, f'Vehicle {vehicle} updated successfully.')
            return redirect('vehicles:detail', pk=vehicle.pk)
    else:
        form = VehicleForm(instance=vehicle)
    context = {
        'form': form,
        'vehicle': vehicle,
        'title': f'Edit {vehicle}',
    }
    return render(request, 'vehicles/form.html', context)


def delete(request: HttpRequest, pk: int) -> HttpResponse:
    """Delete a vehicle."""
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        vehicle_name = str(vehicle)
        vehicle.delete()
        messages.success(request, f'Vehicle {vehicle_name} deleted successfully.')
        return redirect('vehicles:list')
    context = {
        'vehicle': vehicle,
    }
    return render(request, 'vehicles/confirm_delete.html', context)


def maintenance_list(request: HttpRequest) -> HttpResponse:
    """Show all maintenance records."""
    maintenance_records = MaintenanceRecord.objects.select_related('vehicle').all()
    context = {
        'maintenance_records': maintenance_records,
    }
    return render(request, 'vehicles/maintenance_list.html', context)


def add_maintenance(request: HttpRequest, vehicle_id: int) -> HttpResponse:
    """Add maintenance record for a vehicle."""
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    if request.method == 'POST':
        form = MaintenanceRecordForm(request.POST, request.FILES)
        if form.is_valid():
            maintenance = form.save(commit=False)
            maintenance.vehicle = vehicle
            maintenance.save()
            messages.success(request, f'Maintenance record added for {vehicle}.')
            return redirect('vehicles:detail', pk=vehicle.pk)
    else:
        form = MaintenanceRecordForm()
    context = {
        'form': form,
        'vehicle': vehicle,
        'title': f'Add Maintenance for {vehicle}',
    }
    return render(request, 'vehicles/maintenance_form.html', context)
