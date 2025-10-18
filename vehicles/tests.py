
from django.test import TestCase
from django.urls import reverse
from .models import Vehicle, TorqueSetting, MaintenanceRecord
import datetime

class VehicleModelTest(TestCase):
    def test_vehicle_creation(self):
        vehicle = Vehicle.objects.create(make='Honda', model='Civic', year=2020, vin='12345678901234567')
        self.assertEqual(str(vehicle), '2020 Honda Civic')

    def test_needs_oil_change(self):
        vehicle = Vehicle.objects.create(
            make='Toyota', model='Camry', year=2021, vin='76543210987654321',
            current_mileage=6000, last_oil_change_mileage=1000
        )
        self.assertTrue(vehicle.needs_oil_change)

class TorqueSettingModelTest(TestCase):
    def setUp(self):
        self.vehicle = Vehicle.objects.create(make='Ford', model='F-150', year=2019, vin='ABCDEF1234567890')

    def test_torque_setting_creation(self):
        torque = TorqueSetting.objects.create(vehicle=self.vehicle, component='Lugs', torque_value='100 ft-lbs')
        self.assertEqual(str(torque), '2019 Ford F-150 - Lugs: 100 ft-lbs')

class MaintenanceRecordModelTest(TestCase):
    def setUp(self):
        self.vehicle = Vehicle.objects.create(make='Chevy', model='Silverado', year=2018, vin='XYZ1234567890ABC')

    def test_maintenance_record_creation(self):
        record = MaintenanceRecord.objects.create(vehicle=self.vehicle, maintenance_type='oil_change', date_performed=datetime.date.today())
        self.assertEqual(str(record), f'2018 Chevy Silverado - Oil Change ({datetime.date.today()})')

class VehicleViewsTest(TestCase):
    def setUp(self):
        self.vehicle = Vehicle.objects.create(make='Nissan', model='Titan', year=2022, vin='NISSAN1234567890')

    def test_vehicle_list_view(self):
        response = self.client.get(reverse('vehicles:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vehicles/index.html')

    def test_vehicle_detail_view(self):
        response = self.client.get(reverse('vehicles:detail', args=[self.vehicle.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vehicles/detail.html')

    def test_vehicle_create_view(self):
        response = self.client.post(reverse('vehicles:create'), {'make': 'Test', 'model': 'Car', 'year': 2023, 'vin': 'TESTVIN123456789', 'vehicle_type': 'car'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Vehicle.objects.filter(vin='TESTVIN123456789').exists())

    def test_vehicle_update_view(self):
        response = self.client.post(reverse('vehicles:update', args=[self.vehicle.pk]), {'make': 'Updated', 'model': 'Car', 'year': 2022, 'vin': 'NISSAN1234567890', 'vehicle_type': 'car'})
        self.assertEqual(response.status_code, 302)
        self.vehicle.refresh_from_db()
        self.assertEqual(self.vehicle.make, 'Updated')

    def test_vehicle_delete_view(self):
        response = self.client.post(reverse('vehicles:delete', args=[self.vehicle.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Vehicle.objects.filter(pk=self.vehicle.pk).exists())

    def test_maintenance_list_view(self):
        response = self.client.get(reverse('vehicles:maintenance_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vehicles/maintenance_list.html')

    def test_add_maintenance_view(self):
        response = self.client.post(reverse('vehicles:add_maintenance', args=[self.vehicle.pk]), {'maintenance_type': 'oil_change', 'date_performed': datetime.date.today()})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(MaintenanceRecord.objects.filter(vehicle=self.vehicle).exists())
