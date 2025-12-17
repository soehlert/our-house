def menu_items(request):
    """Provide menu structure to all templates."""
    return {
        "menu_items": [
            {
                "name": "Appliances",
                "items": [
                    {"name": "View All Appliances", "url": "house:appliance_list"},
                    {"name": "Add Appliance", "url": "house:appliance_create"},
                ],
            },
            {
                "name": "Electrical",
                "sections": [
                    {
                        "title": "Circuits",
                        "items": [
                            {"name": "View All Circuits", "url": "house:circuit_list"},
                            {"name": "Add Circuit", "url": "house:circuit_create"},
                        ],
                    },
                    {
                        "title": "Diagrams",
                        "items": [
                            {
                                "name": "View All Diagrams",
                                "url": "house:circuit_diagram_list",
                            },
                            {
                                "name": "Add Diagram",
                                "url": "house:circuit_diagram_create",
                            },
                        ],
                    },
                    {
                        "title": "Electrical Panels",
                        "items": [
                            {
                                "name": "View All Panels",
                                "url": "house:electrical_panel_list",
                            },
                            {
                                "name": "Add Panel",
                                "url": "house:electrical_panel_create",
                            },
                        ],
                    },
                    {
                        "title": "Devices",
                        "items": [
                            {"name": "View All Devices", "url": "house:device_list"},
                            {"name": "Add Device", "url": "house:device_create"},
                        ],
                    },
                ],
            },
            {
                "name": "Locations",
                "sections": [
                    {
                        "title": "Rooms",
                        "items": [
                            {"name": "View All Rooms", "url": "house:room_list"},
                            {"name": "Add Room", "url": "house:room_create"},
                        ],
                    },
                    {
                        "title": "Purchase Locations",
                        "items": [
                            {
                                "name": "View All Purchase Locations",
                                "url": "house:purchase_location_list",
                            },
                            {
                                "name": "Add Purchase Location",
                                "url": "house:purchase_location_create",
                            },
                        ],
                    },
                ],
            },
            {
                "name": "Paint Colors",
                "items": [
                    {"name": "View All Paint Colors", "url": "house:paint_color_list"},
                    {"name": "Add Paint Color", "url": "house:paint_color_create"},
                ],
            },
        ],
        "settings_items": [
            {
                "name": "Data Management",
                "items": [
                    {"name": "Import/Export Data", "url": "house:import_export_data"},
                ],
            }
        ],
    }
