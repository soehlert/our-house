import json
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.contrib import messages
from django.utils import timezone
from tracker.models import (
    Appliance, Circuit, CircuitDiagram, Device, ElectricalPanel, PaintColor, PurchaseLocation, Room
)

import logging

logger = logging.getLogger(__name__)


@staff_member_required
def import_data(request):
    """Import house tracker data from JSON."""

    if request.method == 'GET':
        # Check for messages from session
        if request.session.pop('import_success', False):
            messages.success(request, 'Data imported successfully')
        if request.session.pop('import_error', False):
            error_msg = request.session.pop('import_error_msg', 'Import failed')
            messages.error(request, error_msg)
        if request.session.pop('import_warning', False):
            warning_msg = request.session.pop('import_warning_msg', 'Import completed with warnings')
            messages.warning(request, warning_msg)
        if request.session.pop('import_info', False):
            info_msg = request.session.pop('import_info_msg', 'Import information')
            messages.info(request, info_msg)
        return render(request, 'tracker/import_export.html')

    # For POST requests, always return JSON
    try:
        # Get JSON data from file or text input
        json_data = None

        if 'json_file' in request.FILES:
            file_content = request.FILES['json_file'].read()
            json_data = json.loads(file_content)
        elif 'json_text' in request.POST and request.POST['json_text'].strip():
            text_content = request.POST['json_text'].strip()
            json_data = json.loads(text_content)
        else:
            request.session['import_error'] = True
            request.session['import_error_msg'] = 'No data provided'
            request.session.save()
            return JsonResponse({'success': False, 'error': 'No data provided'})

        # Track import statistics for info/warning messages
        import_stats = {
            'rooms': 0,
            'appliances': 0,
            'circuits': 0,
            'devices': 0,
            'paint_colors': 0,
            'skipped': 0
        }

        if request.POST.get('clear_existing') == 'true':
            logger.info("Clearing existing data")
            Device.objects.all().delete()
            Circuit.objects.all().delete()
            CircuitDiagram.objects.all().delete()
            PaintColor.objects.all().delete()
            Appliance.objects.all().delete()
            ElectricalPanel.objects.all().delete()
            PurchaseLocation.objects.all().delete()
            Room.objects.all().delete()

        # Import in dependency order with statistics
        # Independent models first
        for room_data in json_data.get('rooms', []):
            obj, created = Room.objects.get_or_create(
                pk=room_data['pk'],
                defaults=room_data['fields']
            )
            if created:
                import_stats['rooms'] += 1

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
            try:
                fields = appliance_data['fields'].copy()
                if fields.get('room'):
                    fields['room'] = Room.objects.get(pk=fields['room'])
                if fields.get('purchase_location'):
                    fields['purchase_location'] = PurchaseLocation.objects.get(pk=fields['purchase_location'])
                obj, created = Appliance.objects.get_or_create(
                    pk=appliance_data['pk'],
                    defaults=fields
                )
                if created:
                    import_stats['appliances'] += 1
            except Room.DoesNotExist:
                import_stats['skipped'] += 1
                logger.warning(f"Skipped appliance {appliance_data['pk']} - room not found")

        for circuit_data in json_data.get('circuits', []):
            try:
                fields = circuit_data['fields'].copy()
                # Handle foreign keys
                if fields.get('panel'):
                    fields['panel'] = ElectricalPanel.objects.get(pk=fields['panel'])

                # Remove many-to-many fields for initial creation
                rooms_data = fields.pop('rooms', [])
                diagrams_data = fields.pop('diagrams', [])

                circuit, created = Circuit.objects.get_or_create(
                    pk=circuit_data['pk'],
                    defaults=fields
                )
                if created:
                    import_stats['circuits'] += 1

                # Handle many-to-many relationships
                if rooms_data:
                    circuit.rooms.set(rooms_data)
                if diagrams_data:
                    circuit.diagrams.set(diagrams_data)
            except ElectricalPanel.DoesNotExist:
                import_stats['skipped'] += 1
                logger.warning(f"Skipped circuit {circuit_data['pk']} - panel not found")

        for paint_data in json_data.get('paint_colors', []):
            try:
                fields = paint_data['fields'].copy()
                if fields.get('purchase_location'):
                    fields['purchase_location'] = PurchaseLocation.objects.get(pk=fields['purchase_location'])

                # Remove many-to-many fields for initial creation
                rooms_data = fields.pop('rooms', [])

                paint_color, created = PaintColor.objects.get_or_create(
                    pk=paint_data['pk'],
                    defaults=fields
                )
                if created:
                    import_stats['paint_colors'] += 1

                # Handle many-to-many relationships
                if rooms_data:
                    paint_color.rooms.set(rooms_data)
            except PurchaseLocation.DoesNotExist:
                import_stats['skipped'] += 1
                logger.warning(f"Skipped paint color {paint_data['pk']} - location not found")

        for device_data in json_data.get('devices', []):
            try:
                fields = device_data['fields'].copy()
                if fields.get('room'):
                    fields['room'] = Room.objects.get(pk=fields['room'])
                if fields.get('circuit'):
                    fields['circuit'] = Circuit.objects.get(pk=fields['circuit'])

                obj, created = Device.objects.get_or_create(
                    pk=device_data['pk'],
                    defaults=fields
                )
                if created:
                    import_stats['devices'] += 1
            except (Room.DoesNotExist, Circuit.DoesNotExist):
                import_stats['skipped'] += 1
                logger.warning(f"Skipped device {device_data['pk']} - room or circuit not found")

        # Determine message type based on results
        total_imported = sum(v for k, v in import_stats.items() if k != 'skipped')
        logger.info(f"Import stats: {import_stats}")

        if import_stats['skipped'] > 0 and total_imported > 0:
            # Some items imported, some skipped - warning
            request.session['import_warning'] = True
            request.session['import_warning_msg'] = (
                f'Import completed with warnings. Imported {total_imported} items, '
                f'skipped {import_stats["skipped"]} items due to missing dependencies.'
            )
        elif import_stats['skipped'] > 0 and total_imported == 0:
            # Nothing imported - error
            request.session['import_error'] = True
            request.session['import_error_msg'] = (
                f'Import failed. Skipped {import_stats["skipped"]} items due to missing dependencies.'
            )
        elif total_imported > 0:
            # Everything imported successfully
            if total_imported > 50:
                request.session['import_info'] = True
                request.session['import_info_msg'] = (
                    f'Large import completed successfully. Imported {total_imported} items: '
                    f'{import_stats["rooms"]} rooms, {import_stats["appliances"]} appliances, '
                    f'{import_stats["circuits"]} circuits, {import_stats["devices"]} devices, '
                    f'{import_stats["paint_colors"]} paint colors.'
                )
            else:
                request.session['import_success'] = True
        else:
            request.session['import_info'] = True
            request.session['import_info_msg'] = 'No new data to import.'

        request.session.save()
        return JsonResponse({'success': True, 'message': 'Import completed'})

    except json.JSONDecodeError as e:
        logger.exception("JSON decode error: %s", {str(e)})
        request.session['import_error'] = True
        request.session['import_error_msg'] = f'Invalid JSON format: {str(e)}'
        request.session.save()  # Force save
        return JsonResponse({'success': False, 'error': f'Invalid JSON format: {str(e)}'})


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
        'devices': json.loads(serialize('json', Device.objects.all())),
    }

    response = HttpResponse(
        json.dumps(data, indent=2, default=str),
        content_type='application/json'
    )
    response['Content-Disposition'] = f'attachment; filename="house_data_export_{timezone.now().strftime("%Y%m%d_%H%M%S")}.json"'
    return response
