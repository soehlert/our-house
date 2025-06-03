import logging
from django.core.management.base import BaseCommand
from django.db import transaction
from tracker.models import (
    Room, PurchaseLocation, ElectricalPanel, Appliance,
    PaintColor, CircuitDiagram, Circuit, Outlet
)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Clear all data from the house tracker database'

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Actually perform the deletion (required for safety)',
        )
        parser.add_argument(
            '--show-details',
            action='store_true',
            help='Show detailed breakdown of what will be/was deleted',
        )

    def handle(self, *args, **options) -> None:
        show_details = options['show_details']
        confirm = options['confirm']

        try:
            # Count records
            counts = {
                'rooms': Room.objects.count(),
                'purchase_locations': PurchaseLocation.objects.count(),
                'electrical_panels': ElectricalPanel.objects.count(),
                'appliances': Appliance.objects.count(),
                'paint_colors': PaintColor.objects.count(),
                'circuit_diagrams': CircuitDiagram.objects.count(),
                'circuits': Circuit.objects.count(),
                'outlets': Outlet.objects.count(),
            }

            total_records = sum(counts.values())

            if total_records == 0:
                self.stdout.write(
                    self.style.SUCCESS('Database is already empty!')
                )
                return

            # Show what would be deleted
            if show_details:
                self.stdout.write('Records in database:')
                for model_name, count in counts.items():
                    if count > 0:
                        self.stdout.write(f'  {model_name}: {count}')
                self.stdout.write(f'Total: {total_records} records')

            if not confirm:
                self.stdout.write(
                    self.style.WARNING(
                        f'DRY RUN: Would delete {total_records} records from your house tracker database!\n'
                        'Run with --confirm to actually perform the deletion.\n'
                        'Example: python manage.py clear_database --confirm'
                    )
                )
                return

            # Actually delete the data
            with transaction.atomic():
                self.stdout.write('Deleting data...')

                # Delete models with foreign keys first
                deleted_appliances = Appliance.objects.all().delete()[0]
                deleted_paint_colors = PaintColor.objects.all().delete()[0]
                deleted_circuits = Circuit.objects.all().delete()[0]
                deleted_outlets = Outlet.objects.all().delete()[0]
                deleted_circuit_diagrams = CircuitDiagram.objects.all().delete()[0]
                deleted_electrical_panels = ElectricalPanel.objects.all().delete()[0]
                deleted_purchase_locations = PurchaseLocation.objects.all().delete()[0]

                # Delete rooms last (they're referenced by other models)
                deleted_rooms = Room.objects.all().delete()[0]

                total_deleted = (
                    deleted_rooms + deleted_purchase_locations + deleted_electrical_panels +
                    deleted_appliances + deleted_paint_colors + deleted_circuit_diagrams +
                    deleted_circuits + deleted_outlets
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully deleted {total_deleted} records from the database!'
                    )
                )

                if show_details:
                    self.stdout.write('Deleted:')
                    self.stdout.write(f'  Rooms: {deleted_rooms}')
                    self.stdout.write(f'  Purchase Locations: {deleted_purchase_locations}')
                    self.stdout.write(f'  Electrical Panels: {deleted_electrical_panels}')
                    self.stdout.write(f'  Appliances: {deleted_appliances}')
                    self.stdout.write(f'  Paint Colors: {deleted_paint_colors}')
                    self.stdout.write(f'  Circuit Diagrams: {deleted_circuit_diagrams}')
                    self.stdout.write(f'  Circuits: {deleted_circuits}')
                    self.stdout.write(f'  Outlets: {deleted_outlets}')

        except Exception as e:
            logger.exception('Error clearing database')
            self.stdout.write(
                self.style.ERROR(f'Error clearing database: {e}')
            )
            raise