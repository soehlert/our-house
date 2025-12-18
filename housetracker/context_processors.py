from django.urls import reverse_lazy

def menu_items(request):
    """Provide menu structure to all templates."""
    return {
        "menu_items": [
            {"name": "Appliances", "items": [
                {"name": "View All Appliances", "url": reverse_lazy("house:appliance_list")},
                {"name": "Add Appliance", "url": reverse_lazy("house:appliance_create")}
            ]},
            {"name": "Vehicles", "items": [
                {"name": "View All Vehicles", "url": reverse_lazy("vehicles:vehicle_list")},
                {"name": "Add Vehicle", "url": reverse_lazy("vehicles:vehicle_create")}
            ]},
            {"name": "Electrical", "sections": [
                {"title": "Circuits", "items": [
                    {"name": "View All Circuits", "url": reverse_lazy("house:circuit_list")},
                    {"name": "Add Circuit", "url": reverse_lazy("house:circuit_create")}
                ]},
                {"title": "Diagrams", "items": [
                    {"name": "View All Diagrams", "url": reverse_lazy("house:circuit_diagram_list")},
                    {"name": "Add Diagram", "url": reverse_lazy("house:circuit_diagram_create")}
                ]},
                {"title": "Electrical Panels", "items": [
                    {"name": "View All Panels", "url": reverse_lazy("house:electrical_panel_list")},
                    {"name": "Add Panel", "url": reverse_lazy("house:electrical_panel_create")}
                ]},
                {"title": "Devices", "items": [
                    {"name": "View All Devices", "url": reverse_lazy("house:device_list")},
                    {"name": "Add Device", "url": reverse_lazy("house:device_create")}
                ]}
            ]},
            {"name": "Locations", "sections": [
                {"title": "Rooms", "items": [
                    {"name": "View All Rooms", "url": reverse_lazy("house:room_list")},
                    {"name": "Add Room", "url": reverse_lazy("house:room_create")}
                ]},
                {"title": "Purchase Locations", "items": [
                    {"name": "View All Purchase Locations", "url": reverse_lazy("house:purchase_location_list")},
                    {"name": "Add Purchase Location", "url": reverse_lazy("house:purchase_location_create")}
                ]}
            ]},
            {"name": "Paint Colors", "items": [
                {"name": "View All Paint Colors", "url": reverse_lazy("house:paint_color_list")},
                {"name": "Add Paint Color", "url": reverse_lazy("house:paint_color_create")}
            ]}
        ],
        "settings_items": [
            {"name": "Data Management", "items": [
                {"name": "Import/Export Data", "url": reverse_lazy("house:import_export_data")}
            ]}
        ]
    }
