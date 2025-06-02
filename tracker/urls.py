from django.urls import path
from tracker.views import home_views, appliance_views, circuit_diagram_views, circuit_views, electric_panel_views, outlet_views, paint_color_views, purchase_location_views, room_views

app_name = 'tracker'

urlpatterns = [
    path('', home_views.home, name='home'),

    # Alert card URLs
    path('alerts/missing-docs/', home_views.missing_docs_list, name='missing_docs_list'),
    path('alerts/expiring-warranties/', home_views.expiring_warranties_list, name='expiring_warranties_list'),
    path('alerts/unmapped-rooms/', home_views.unmapped_rooms_list, name='unmapped_rooms_list'),
    path('alerts/recent-additions/', home_views.recent_additions_list, name='recent_additions_list'),

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

    # Electric Panel URLs
    path('electric-panels/', electric_panel_views.electric_panel_list, name='electric_panel_list'),
    path('electric-panels/<int:pk>/', electric_panel_views.electric_panel_detail, name='electric_panel_detail'),
    path('electric-panels/create/', electric_panel_views.electric_panel_create, name='electric_panel_create'),
    path('electric-panels/<int:pk>/update/', electric_panel_views.electric_panel_update, name='electric_panel_update'),
    path('electric-panels/<int:pk>/delete/', electric_panel_views.electric_panel_delete, name='electric_panel_delete'),

    # Outlet URLs
    path('outlets/', outlet_views.outlet_list, name='outlet_list'),
    path('outlets/<int:pk>/', outlet_views.outlet_detail, name='outlet_detail'),
    path('outlets/create/', outlet_views.outlet_create, name='outlet_create'),
    path('outlets/<int:pk>/edit/', outlet_views.outlet_update, name='outlet_update'),
    path('outlets/<int:pk>/delete/', outlet_views.outlet_delete, name='outlet_delete'),

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
