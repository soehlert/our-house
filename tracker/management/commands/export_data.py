import json
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.core.serializers import serialize
from tracker.models import (
    Appliance, Circuit, CircuitDiagram, Device, ElectricalPanel, PaintColor, PurchaseLocation, Room
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
            'appliances': json.loads(serialize('json', Appliance.objects.all())),
            'circuits': json.loads(serialize('json', Circuit.objects.all())),
            'circuit_diagrams': json.loads(serialize('json', CircuitDiagram.objects.all())),
            'devices': json.loads(serialize('json', Device.objects.all())),
            'electrical_panels': json.loads(serialize('json', ElectricalPanel.objects.all())),
            'export_date': timezone.now().isoformat(),
            'paint_colors': json.loads(serialize('json', PaintColor.objects.all())),
            'purchase_locations': json.loads(serialize('json', PurchaseLocation.objects.all())),
            'rooms': json.loads(serialize('json', Room.objects.all())),
        }

        output_file = options['output']

        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)

        self.stdout.write(
            self.style.SUCCESS(f'Successfully exported data to {output_file}')
        )
