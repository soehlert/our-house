from django.contrib import admin
from .models import Appliance, Circuit, CircuitDiagram, ElectricalPanel, Outlet, PaintColor, PurchaseLocation, Room


@admin.register(Appliance)
class ApplianceAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'model_number', 'appliance_type', 'room', 'registered']
    list_filter = ['appliance_type', 'registered', 'room']
    search_fields = ['name', 'brand', 'model_number', 'serial_number']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Circuit)
class CircuitAdmin(admin.ModelAdmin):
    list_display = ['circuit_number', 'description', 'breaker_size', 'pole_type', 'protection_type', 'panel']
    list_filter = ['breaker_size', 'pole_type', 'protection_type', 'panel']
    search_fields = ['circuit_number', 'description']
    filter_horizontal = ['rooms', 'diagrams']


@admin.register(CircuitDiagram)
class CircuitDiagramAdmin(admin.ModelAdmin):
    list_display = ['description', 'created_at']
    readonly_fields = ['created_at']


@admin.register(ElectricalPanel)
class ElectricalPanelAdmin(admin.ModelAdmin):
    list_display = ["brand", "model", "kind", "breaker_type", "description"]
    list_filter = ["kind", "breaker_type"]
    search_fields = ["brand", "model", "kind", "breaker_type"]


@admin.register(Outlet)
class OutletAdmin(admin.ModelAdmin):
    list_display = ['device_type', 'room', 'circuit', 'position_number', 'location_description', 'protection_type']
    list_filter = ['device_type', 'room', 'circuit', 'protection_type']
    search_fields = ['location_description', 'room__name', 'circuit__description']


@admin.register(PaintColor)
class PaintColorAdmin(admin.ModelAdmin):
    list_display = ['paint_color', 'paint_code', 'paint_brand', 'purchase_date']
    list_filter = ['paint_brand', 'paint_base', 'finish_type']
    search_fields = ['paint_color', 'paint_code']
    filter_horizontal = ['rooms']


@admin.register(PurchaseLocation)
class PurchaseLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'website', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name', 'location_description']