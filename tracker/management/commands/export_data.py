import json
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.core.serializers import serialize
from tracker.models import (
    Room, PurchaseLocation, ElectricalPanel, Appliance,
    PaintColor, CircuitDiagram, Circuit, Outlet
)


class Command(BaseCommand):
    help = 'Export all tracker data to JSON'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            help='Output file path',
            default='house_data_export.json',
)


    def handle(self, *args, **options):
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

        output_file = options['output']

        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)

        self.stdout.write(
            self.style.SUCCESS(f'Successfully exported data to {output_file}')
        )
