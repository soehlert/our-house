from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Count, Q

import logging

from tracker.models import Outlet, Room
from tracker.forms import OutletForm

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def outlet_list(request):
    """List all outlets grouped by room."""
    from django.db.models import Count, Q

    # Get rooms with their outlet counts and prefetch outlets
    rooms_with_outlets = Room.objects.prefetch_related(
        'outlets__circuit'
    ).annotate(
        outlet_count=Count('outlets'),
        receptacle_count=Count('outlets', filter=Q(outlets__device_type='RECEPTACLE')),
        switch_count=Count('outlets', filter=Q(outlets__device_type='SWITCH')),
        light_count=Count('outlets', filter=Q(outlets__device_type='LIGHT'))
    ).filter(
        outlet_count__gt=0
    ).order_by('name')

    search_query = request.GET.get('search', '').strip()
    logger.info(f"Search query: '{search_query}'")

    if search_query:
        logger.info("Entering search mode")
        # If searching, show individual outlets like before
        outlets = Outlet.objects.select_related('room', 'circuit').filter(
            Q(device_type__icontains=search_query) |
            Q(room__name__icontains=search_query) |
            Q(circuit__description__icontains=search_query) |
            Q(location_description__icontains=search_query)
        ).distinct()

        logger.info(f"Found {outlets.count()} outlets")
        logger.info(f"SQL query: {outlets.query}")

        return render(request, 'tracker/outlets/list.html', {
            "object_list": outlets,
            "search_mode": True,
        })

    return render(request, 'tracker/outlets/list.html', {
        "rooms_with_outlets": rooms_with_outlets,
        "search_mode": False,
    })



def outlet_list_by_room_api(request, room_id):
    """API endpoint to get outlets for a specific room."""
    room = get_object_or_404(Room, id=room_id)
    outlets = Outlet.objects.filter(room=room).select_related('circuit').order_by('device_type', 'location_description')

    outlet_data = []
    for outlet in outlets:
        circuit_data = None
        if outlet.circuit:
            circuit_data = {
                'circuit_number': outlet.circuit.circuit_number,
                'pole_type_display': outlet.circuit.get_pole_type_display(),
                'gfci': outlet.circuit.gfci,
                'afci': outlet.circuit.afci,
                'cafi': outlet.circuit.cafi,
            }

        outlet_data.append({
            'id': outlet.id,
            'device_type': outlet.device_type,
            'device_type_display': outlet.get_device_type_display(),
            'location_description': outlet.location_description,
            'position_number': outlet.position_number,
            'circuit': circuit_data,
        })

    return JsonResponse({
        'room': {'id': room.id, 'name': room.name},
        'outlets': outlet_data
    })



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
            messages.success(request, f'Outlet "{outlet.location_description}" created successfully.')
            if 'save_and_add_another' in request.POST:
                return redirect('tracker:outlet_create')
            else:
                return redirect('tracker:outlet_detail', pk=outlet.pk)
    else:
        # Pre-select room if provided in URL
        initial_data = {}
        room_id = request.GET.get('room')
        if room_id:
            initial_data['room'] = room_id

        form = OutletForm(initial=initial_data)

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
