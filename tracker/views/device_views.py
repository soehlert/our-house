from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Count, Q

import logging

from tracker.models import Device, Room
from tracker.forms import DeviceForm

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def device_list(request):
    """List all devices grouped by room."""
    from django.db.models import Count, Q

    # Get rooms with their device counts and prefetch devices
    rooms_with_devices = Room.objects.prefetch_related(
        'devices__circuit'
    ).annotate(
        device_count=Count('devices'),
        receptacle_count=Count('devices', filter=Q(devices__device_type='Receptacle')),
        switch_count=Count('devices', filter=Q(devices__device_type='Switch')),
        light_count=Count('devices', filter=Q(devices__device_type='Light'))
    ).filter(
        device_count__gt=0
    ).order_by('name')

    search_query = request.GET.get('search', '').strip()
    logger.info(f"Search query: '{search_query}'")

    if search_query:
        logger.info("Entering search mode")
        # If searching, show individual devices like before
        devices = Device.objects.select_related('room', 'circuit').filter(
            Q(device_type__icontains=search_query) |
            Q(room__name__icontains=search_query) |
            Q(circuit__description__icontains=search_query) |
            Q(location_description__icontains=search_query)
        ).distinct()

        logger.info(f"Found {devices.count()} devices")
        logger.info(f"SQL query: {devices.query}")

        return render(request, 'tracker/devices/list.html', {
            "object_list": devices,
            "search_mode": True,
        })

    return render(request, 'tracker/devices/list.html', {
        "rooms_with_devices": rooms_with_devices,
        "search_mode": False,
    })


def device_list_by_room_api(request, room_id):
    """API endpoint to get devices for a specific room."""
    room = get_object_or_404(Room, id=room_id)
    devices = Device.objects.filter(room=room).select_related('circuit').order_by('device_type', 'location_description')

    device_data = []
    for device in devices:
        circuit_data = None
        if device.circuit:
            circuit_data = {
                'circuit_number': device.circuit.circuit_number,
                'pole_type_display': device.circuit.get_pole_type_display(),
            }

        device_data.append({
            'id': device.id,
            'attached_appliance': device.attached_appliance.name if device.attached_appliance else None,
            'device_type': device.device_type,
            'device_type_display': device.get_device_type_display(),
            'location_description': device.location_description,
            'position_number': device.position_number,
            'protection_type': device.protection_type,
            'circuit': circuit_data,
        })

    return JsonResponse({
        'room': {'id': room.id, 'name': room.name},
        'devices': device_data
    })



def device_detail(request, pk):
    """Display device details."""
    device = get_object_or_404(Device.objects.select_related('room'), pk=pk)

    context = {
        'device': device,
    }

    return render(request, 'tracker/devices/detail.html', context)


def device_create(request):
    """Create a new device."""
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            device = form.save()
            messages.success(request, f'Device "{device.location_description}" created successfully.')
            if 'save_and_add_another' in request.POST:
                return redirect('tracker:device_create')
            else:
                return redirect('tracker:device_detail', pk=device.pk)
    else:
        # Pre-select room if provided in URL
        initial_data = {}
        room_id = request.GET.get('room')
        if room_id:
            initial_data['room'] = room_id

        form = DeviceForm(initial=initial_data)

    return render(request, 'tracker/devices/form.html', {
        'form': form,
        'device': None
    })



def device_update(request, pk):
    """Update an existing device."""
    device = get_object_or_404(Device, pk=pk)

    if request.method == 'POST':
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            device = form.save()
            messages.success(request, f'Device in {device.room.name} updated successfully.')
            return redirect('tracker:device_detail', pk=device.pk)
    else:
        form = DeviceForm(instance=device)

    return render(request, 'tracker/devices/form.html', {
        'form': form,
        'device': device
    })


def device_delete(request, pk):
    """Delete an device."""
    device = get_object_or_404(Device, pk=pk)

    if request.method == 'POST':
        device_info = f"{device.get_device_type_display()} in {device.room.name}"
        device.delete()
        messages.success(request, f'Device "{device_info}" deleted successfully.')
        return redirect('tracker:device_list')

    return render(request, 'tracker/devices/confirm_delete.html', {
        'device': device
    })
