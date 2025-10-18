from django.contrib import admin
from vehicles.models import Vehicle, TorqueSetting, MaintenanceRecord


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['year', 'make', 'model', 'vehicle_type', 'current_mileage', 'needs_oil_change']
    list_filter = ['vehicle_type', 'make', 'year']
    search_fields = ['make', 'model', 'vin']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(TorqueSetting)
class TorqueSettingAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'component', 'torque_value']
    list_filter = ['vehicle']
    search_fields = ['component', 'vehicle__make', 'vehicle__model']


@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'maintenance_type', 'date_performed', 'mileage', 'cost']
    list_filter = ['maintenance_type', 'date_performed', 'vehicle']
    search_fields = ['vehicle__make', 'vehicle__model', 'description']
    date_hierarchy = 'date_performed'
