from django.urls import path
from house.views import home_views, import_export_views, appliance_views, circuit_diagram_views, circuit_views, electrical_panel_views, device_views, paint_color_views, purchase_location_views, room_views

app_name = 'house'

urlpatterns = [
    path('', home_views.home, name='home'),

    # Alert card URLs
    path('alerts/missing-docs/', home_views.missing_docs_list, name='missing_docs_list'),
    path('alerts/expiring-warranties/', home_views.expiring_warranties_list, name='expiring_warranties_list'),
    path('alerts/unmapped-rooms/', home_views.unmapped_rooms_list, name='unmapped_rooms_list'),
    path('alerts/unassigned-devices/', home_views.unassigned_devices_list, name='unassigned_devices_list'),
    path('dismiss-warranty/<int:appliance_id>/', home_views.dismiss_warranty_alert, name='dismiss_warranty_alert'),
    path('undismiss-warranty/<int:appliance_id>/', home_views.undismiss_warranty_alert, name='undismiss_warranty_alert'),

    # Appliance URLs
    path('appliances/', appliance_views.appliance_list, name='appliance_list'),
    path('appliances/<int:pk>/', appliance_views.appliance_detail, name='appliance_detail'),
    path('appliances/create/', appliance_views.appliance_create, name='appliance_create'),
    path('appliances/<int:pk>/update/', appliance_views.appliance_update, name='appliance_update'),
    path('appliances/<int:pk>/delete/', appliance_views.appliance_delete, name='appliance_delete'),

    # Circuit URLs
    path('circuits/', circuit_views.circuit_list, name='circuit_list'),
    path('circuits/<int:pk>/', circuit_views.circuit_detail, name='circuit_detail'),
    path('circuits/create/', circuit_views.circuit_create, name='circuit_create'),
    path('circuits/<int:pk>/update/', circuit_views.circuit_update, name='circuit_update'),
    path('circuits/<int:pk>/delete/', circuit_views.circuit_delete, name='circuit_delete'),

    # Circuit Diagram URLs
    path('circuit-diagrams/', circuit_diagram_views.circuit_diagram_list, name='circuit_diagram_list'),
    path('circuit-diagrams/<int:pk>/', circuit_diagram_views.circuit_diagram_detail, name='circuit_diagram_detail'),
    path('circuit-diagrams/create/', circuit_diagram_views.circuit_diagram_create, name='circuit_diagram_create'),
    path('circuit-diagrams/<int:pk>/update/', circuit_diagram_views.circuit_diagram_update, name='circuit_diagram_update'),
    path('circuit-diagrams/<int:pk>/delete/', circuit_diagram_views.circuit_diagram_delete, name='circuit_diagram_delete'),

    # Data Management
    path('export/', import_export_views.export_data, name='export_data'),
    path('data-management/', import_export_views.import_data, name='import_export_data'),

    # Device URLs
    path('devices/', device_views.device_list, name='device_list'),
    path('devices/<int:pk>/', device_views.device_detail, name='device_detail'),
    path('devices/create/', device_views.device_create, name='device_create'),
    path('devices/<int:pk>/edit/', device_views.device_update, name='device_update'),
    path('devices/<int:pk>/delete/', device_views.device_delete, name='device_delete'),
    path('devices/room/<int:room_id>/api/', device_views.device_list_by_room_api, name='device_list_by_room'),

    # Electrical Panel URLs
    path('electrical-panels/', electrical_panel_views.electrical_panel_list, name='electrical_panel_list'),
    path('electrical-panels/<int:pk>/', electrical_panel_views.electrical_panel_detail, name='electrical_panel_detail'),
    path('electrical-panels/create/', electrical_panel_views.electrical_panel_create, name='electrical_panel_create'),
    path('electrical-panels/<int:pk>/update/', electrical_panel_views.electrical_panel_update, name='electrical_panel_update'),
    path('electrical-panels/<int:pk>/delete/', electrical_panel_views.electrical_panel_delete, name='electrical_panel_delete'),

    # Paint Color URLs
    path('paint-colors/', paint_color_views.paint_color_list, name='paint_color_list'),
    path('paint-colors/<int:pk>/', paint_color_views.paint_color_detail, name='paint_color_detail'),
    path('paint-colors/create/', paint_color_views.paint_color_create, name='paint_color_create'),
    path('paint-colors/<int:pk>/update/', paint_color_views.paint_color_update, name='paint_color_update'),
    path('paint-colors/<int:pk>/delete/', paint_color_views.paint_color_delete, name='paint_color_delete'),

    # Purchase Location URLs
    path('purchase-locations/', purchase_location_views.purchase_location_list, name='purchase_location_list'),
    path('purchase-locations/<int:pk>/', purchase_location_views.purchase_location_detail, name='purchase_location_detail'),
    path('purchase-locations/create/', purchase_location_views.purchase_location_create, name='purchase_location_create'),
    path('purchase-locations/<int:pk>/update/', purchase_location_views.purchase_location_update, name='purchase_location_update'),
    path('purchase-locations/<int:pk>/delete/', purchase_location_views.purchase_location_delete, name='purchase_location_delete'),

    # Room URLs
    path('rooms/', room_views.room_list, name='room_list'),
    path('rooms/<int:pk>/', room_views.room_detail, name='room_detail'),
    path('rooms/create/', room_views.room_create, name='room_create'),
    path('rooms/<int:pk>/update/', room_views.room_update, name='room_update'),
    path('rooms/<int:pk>/delete/', room_views.room_delete, name='room_delete'),
]
