from django.contrib import admin
from .models import Vehicle

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name', 'make', 'model', 'year', 'vin', 'license_plate')
    search_fields = ('name', 'make', 'model', 'vin', 'license_plate')
    list_filter = ('make', 'year', 'purchase_location')