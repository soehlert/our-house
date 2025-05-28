from django.contrib import admin
from .models import Room, Appliance, PaintColor, Circuit, CircuitDiagram, PurchaseLocation


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(PurchaseLocation)
class PurchaseLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'website', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Appliance)
class ApplianceAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'model_number', 'appliance_type', 'room', 'registered']
    list_filter = ['appliance_type', 'registered', 'room']
    search_fields = ['name', 'brand', 'model_number', 'serial_number']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(PaintColor)
class PaintColorAdmin(admin.ModelAdmin):
    list_display = ['paint_color', 'paint_code', 'paint_brand', 'purchase_date']
    list_filter = ['paint_brand', 'purchase_date']
    search_fields = ['paint_color', 'paint_code']
    filter_horizontal = ['rooms']


@admin.register(Circuit)
class CircuitAdmin(admin.ModelAdmin):
    list_display = ['circuit_number', 'description', 'breaker_size', 'pole_type', 'gfci', 'afci']
    list_filter = ['breaker_size', 'pole_type', 'gfci', 'afci', 'cafi']
    search_fields = ['circuit_number', 'description']
    filter_horizontal = ['rooms', 'diagrams']


@admin.register(CircuitDiagram)
class CircuitDiagramAdmin(admin.ModelAdmin):
    list_display = ['description', 'created_at']
    readonly_fields = ['created_at']
