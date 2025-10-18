from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import render, get_object_or_404
from django.apps import apps
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
import json
from django.core.serializers import serialize

from house.models import Appliance, Circuit, Device, PaintColor, PurchaseLocation, Room
from vehicles.models import Vehicle


def _get_warranty_data():
    """Helper function to get warranty expiration data."""
    today = timezone.now().date()

    expired_appliances = Appliance.objects.filter(
        warranty_expires__lt=today,
        warranty_expires__isnull=False,
        warranty_alert_dismissed=False
    ).order_by('warranty_expires')

    expiring_appliances = Appliance.objects.filter(
        warranty_expires__gte=today,
        warranty_expires__lte=today + timedelta(days=90),
        warranty_alert_dismissed=False
    ).order_by('warranty_expires')

    return {
        'expired_appliances': expired_appliances,
        'expiring_appliances': expiring_appliances,
        'total_count': expired_appliances.count() + expiring_appliances.count(),
    }


@require_POST
def dismiss_warranty_alert(request, appliance_id):
    """Dismiss a warranty alert for a specific appliance."""
    appliance = get_object_or_404(Appliance, id=appliance_id)
    appliance.warranty_alert_dismissed = True
    appliance.warranty_alert_dismissed_at = timezone.now()
    appliance.save(update_fields=['warranty_alert_dismissed', 'warranty_alert_dismissed_at'])

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})

    return redirect('house:expiring_warranties_list')


@require_POST
def undismiss_warranty_alert(request, appliance_id):
    """Un-dismiss a warranty alert for a specific appliance."""
    appliance = get_object_or_404(Appliance, id=appliance_id)
    appliance.warranty_alert_dismissed = False
    appliance.warranty_alert_dismissed_at = None
    appliance.save(update_fields=['warranty_alert_dismissed', 'warranty_alert_dismissed_at'])

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})

    return redirect('house:expiring_warranties_list')

def unassigned_devices_list(request):
    """Show devices not assigned to any circuit."""
    devices = Device.objects.filter(circuit__isnull=True).order_by('room__name', 'device_type')

    context = {
        'object_list': devices,
        'show_create_button': False
    }
    return render(request, 'house/alert_cards/unassigned_devices_list.html', context)


def home(request):
    """Home page showing overview of all data."""

    vehicles_needing_service = Vehicle.objects.filter(
        current_mileage__isnull=False,
        last_oil_change_mileage__isnull=False
    ).extra(
        where=["current_mileage - last_oil_change_mileage >= 5000"]
    )

    # Expiring warranties (next 90 days) ignoring appliances without a warranty date
    warranty_data = _get_warranty_data()

    # Rooms with no circuits or devices mapped
    unmapped_rooms = Room.objects.filter(
        Q(circuits__isnull=True) & Q(devices__isnull=True)
    ).distinct().count()

    # Devices not assigned to any circuit
    unassigned_devices = Device.objects.filter(circuit__isnull=True).count()

    # Appliances without a manual
    missing_docs = Appliance.objects.filter(owners_manual='').count()

    # Get recent items for activity feed
    recent_items = []
    for model_name in ['Appliance', 'Room', 'Circuit', 'Device', 'PaintColor']:
        try:
            model = apps.get_model('house', model_name)
            items = model.objects.order_by('-created_at')[:2]
            for item in items:
                recent_items.append({
                    'name': str(item),
                    'model_name': model_name,
                    'created_at': item.created_at
                })
        except LookupError:
            # Skip if model doesn't exist yet
            continue

    # Sort by creation date and limit
    recent_items = sorted(recent_items, key=lambda x: x['created_at'], reverse=True)[:10]

    context = {
        'room_count': Room.objects.count(),
        'appliance_count': Appliance.objects.count(),
        'location_count': PurchaseLocation.objects.count(),
        'paint_color_count': PaintColor.objects.count(),
        'circuit_count': Circuit.objects.count(),
        'unmapped_rooms_count': unmapped_rooms,
        'unassigned_devices_count': unassigned_devices,
        'missing_docs_count': missing_docs,
        'recent_items': recent_items,
        **warranty_data,
        'vehicle_count': Vehicle.objects.count(),
        'vehicles_needing_service': vehicles_needing_service,
    }
    return render(request, 'house/home.html', context)


def missing_docs_list(request):
    """Show appliances missing documentation."""
    appliances = Appliance.objects.filter(owners_manual='').order_by('name')
    context = {
        'appliances': appliances,
        'show_create_button': False
    }
    return render(request, 'house/alert_cards/missing_docs_list.html', context)

def expiring_warranties_list(request):
    """Show appliances with expiring or expired warranties."""
    today = timezone.now().date()

    warranty_data = _get_warranty_data()
    warranty_data['show_create_button'] = False

    dismissed_count = Appliance.objects.filter(
        warranty_alert_dismissed=True,
        warranty_expires__isnull=False
    ).count()

    # Get dismissed appliances to show when requested
    dismissed_expired = Appliance.objects.filter(
        warranty_expires__lt=today,
        warranty_expires__isnull=False,
        warranty_alert_dismissed=True
    ).order_by('warranty_expires')

    dismissed_expiring = Appliance.objects.filter(
        warranty_expires__gte=today,
        warranty_expires__lte=today + timedelta(days=90),
        warranty_alert_dismissed=True
    ).order_by('warranty_expires')

    warranty_data.update({
        'dismissed_expired': dismissed_expired,
        'dismissed_expiring': dismissed_expiring,
        'dismissed_count': dismissed_count,
    })

    context = {
        **warranty_data,
    }
    return render(request, 'house/alert_cards/warranty_expiration_list.html', context)


def unmapped_rooms_list(request):
    """Show rooms with no circuits or devices mapped."""
    rooms = Room.objects.filter(
        Q(circuits__isnull=True) & Q(devices__isnull=True)
    ).distinct().order_by('name')

    context = {
        'rooms': rooms,
        'show_create_button': False
    }
    return render(request, 'house/alert_cards/unmapped_rooms_list.html', context)


@staff_member_required
def export_data(request):
    """Export all house house data as JSON."""
    data = {
        'export_date': timezone.now().isoformat(),
        'rooms': json.loads(serialize('json', Room.objects.all())),
        'purchase_locations': json.loads(serialize('json', PurchaseLocation.objects.all())),
        'electrical_panels': json.loads(serialize('json', ElectricalPanel.objects.all())),
        'appliances': json.loads(serialize('json', Appliance.objects.all())),
        'paint_colors': json.loads(serialize('json', PaintColor.objects.all())),
        'circuit_diagrams': json.loads(serialize('json', CircuitDiagram.objects.all())),
        'circuits': json.loads(serialize('json', Circuit.objects.all())),
        'devices': json.loads(serialize('json', Device.objects.all())),
    }

    response = HttpResponse(
        json.dumps(data, indent=2, default=str),
        content_type='application/json'
    )
    response['Content-Disposition'] = f'attachment; filename="house_data_export_{timezone.now().strftime("%Y%m%d_%H%M%S")}.json"'
    return response

@staff_member_required
@require_http_methods(["POST"])
def import_data(request):
    """Import house house data from JSON."""
    try:
        if 'json_file' in request.FILES:
            json_data = json.loads(request.FILES['json_file'].read())
        elif 'json_text' in request.POST:
            json_data = json.loads(request.POST['json_text'])
        else:
            return JsonResponse({'success': False, 'error': 'No data provided'})

        # Clear existing data if requested
        if request.POST.get('clear_existing') == 'true':
            device.objects.all().delete()
            Circuit.objects.all().delete()
            CircuitDiagram.objects.all().delete()
            PaintColor.objects.all().delete()
            Appliance.objects.all().delete()
            ElectricalPanel.objects.all().delete()
            PurchaseLocation.objects.all().delete()
            Room.objects.all().delete()

        # Import in dependency order
        # 1. Independent models first
        for room_data in json_data.get('rooms', []):
            Room.objects.get_or_create(
                pk=room_data['pk'],
                defaults=room_data['fields']
            )

        for location_data in json_data.get('purchase_locations', []):
            PurchaseLocation.objects.get_or_create(
                pk=location_data['pk'],
                defaults=location_data['fields']
            )

        for panel_data in json_data.get('electrical_panels', []):
            ElectricalPanel.objects.get_or_create(
                pk=panel_data['pk'],
                defaults=panel_data['fields']
            )

        for diagram_data in json_data.get('circuit_diagrams', []):
            CircuitDiagram.objects.get_or_create(
                pk=diagram_data['pk'],
                defaults=diagram_data['fields']
            )

        # 2. Models with foreign keys
        for appliance_data in json_data.get('appliances', []):
            fields = appliance_data['fields'].copy()
            if fields.get('room'):
                fields['room'] = Room.objects.get(pk=fields['room'])
            if fields.get('purchase_location'):
                fields['purchase_location'] = PurchaseLocation.objects.get(pk=fields['purchase_location'])
            Appliance.objects.get_or_create(
                pk=appliance_data['pk'],
                defaults=fields
            )

        for circuit_data in json_data.get('circuits', []):
            fields = circuit_data['fields'].copy()
            # Handle foreign keys
            if fields.get('panel'):
                fields['panel'] = ElectricalPanel.objects.get(pk=fields['panel'])

            # Remove many-to-many fields for initial creation
            rooms_data = fields.pop('rooms', [])
            diagrams_data = fields.pop('diagrams', [])

            circuit = Circuit.objects.get_or_create(
                pk=circuit_data['pk'],
                defaults=fields
            )[0]

            # Handle many-to-many relationships
            if rooms_data:
                circuit.rooms.set(rooms_data)
            if diagrams_data:
                circuit.diagrams.set(diagrams_data)

        for paint_data in json_data.get('paint_colors', []):
            fields = paint_data['fields'].copy()
            if fields.get('purchase_location'):
                fields['purchase_location'] = PurchaseLocation.objects.get(pk=fields['purchase_location'])

            # Remove many-to-many fields for initial creation
            rooms_data = fields.pop('rooms', [])

            paint_color = PaintColor.objects.get_or_create(
                pk=paint_data['pk'],
                defaults=fields
            )[0]

            # Handle many-to-many relationships
            if rooms_data:
                paint_color.rooms.set(rooms_data)

        for device_data in json_data.get('devices', []):
            fields = device_data['fields'].copy()
            if fields.get('room'):
                fields['room'] = Room.objects.get(pk=fields['room'])
            if fields.get('circuit'):
                fields['circuit'] = Circuit.objects.get(pk=fields['circuit'])

            Device.objects.get_or_create(
                pk=device_data['pk'],
                defaults=fields
            )

        return JsonResponse({'success': True, 'message': 'Data imported successfully'})

    except Exception as e:
        logger.exception("Error importing data")
        return JsonResponse({'success': False, 'error': str(e)})