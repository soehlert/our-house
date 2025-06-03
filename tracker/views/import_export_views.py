import json
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.utils import timezone
from tracker.models import (
    Room, PurchaseLocation, ElectricalPanel, Appliance,
    PaintColor, CircuitDiagram, Circuit, Outlet
)
import logging

logger = logging.getLogger(__name__)


@staff_member_required
def import_data(request):
    """Import house tracker data from JSON."""
    if request.method == 'GET':
        return render(request, 'tracker/import_export.html')
    try:
        if 'json_file' in request.FILES:
            json_data = json.loads(request.FILES['json_file'].read())
        elif 'json_text' in request.POST:
            json_data = json.loads(request.POST['json_text'])
        else:
            return JsonResponse({'success': False, 'error': 'No data provided'})

        # Clear existing data if requested
        if request.POST.get('clear_existing') == 'true':
            Outlet.objects.all().delete()
            Circuit.objects.all().delete()
            CircuitDiagram.objects.all().delete()
            PaintColor.objects.all().delete()
            Appliance.objects.all().delete()
            ElectricalPanel.objects.all().delete()
            PurchaseLocation.objects.all().delete()
            Room.objects.all().delete()

        # Import in dependency order
        # Independent models first
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

        # Models with foreign keys
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

        for outlet_data in json_data.get('outlets', []):
            fields = outlet_data['fields'].copy()
            if fields.get('room'):
                fields['room'] = Room.objects.get(pk=fields['room'])
            if fields.get('circuit'):
                fields['circuit'] = Circuit.objects.get(pk=fields['circuit'])

            Outlet.objects.get_or_create(
                pk=outlet_data['pk'],
                defaults=fields
            )

        return JsonResponse({'success': True, 'message': 'Data imported successfully'})

    except Exception as e:
        logger.exception("Error importing data")
        return JsonResponse({'success': False, 'error': str(e)})


@staff_member_required
def export_data(request):
    """Export all house tracker data as JSON."""
    data = {
        'export_date': timezone.now().isoformat(),
        'rooms': json.loads(serialize('json', Room.objects.all())),
        'purchase_locations': json.loads(serialize('json', PurchaseLocation.objects.all())),
        'electrical_panels': json.loads(serialize('json', ElectricalPanel.objects.all())),
        'appliances': json.loads(serialize('json', Appliance.objects.all())),
        'paint_colors': json.loads(serialize('json', PaintColor.objects.all())),
        'circuit_diagrams': json.loads(serialize('json', CircuitDiagram.objects.all())),
        'circuits': json.loads(serialize('json', Circuit.objects.all())),
        'outlets': json.loads(serialize('json', Outlet.objects.all())),
    }

    response = HttpResponse(
        json.dumps(data, indent=2, default=str),
        content_type='application/json'
    )
    response['Content-Disposition'] = f'attachment; filename="house_data_export_{timezone.now().strftime("%Y%m%d_%H%M%S")}.json"'
    return response
