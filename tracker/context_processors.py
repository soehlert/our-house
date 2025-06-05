def menu_items(request):
    """Provide menu structure to all templates."""
    return {
        'menu_items': [
            {
                'name': 'Appliances',
                'items': [
                    {'name': 'View All Appliances', 'url': 'tracker:appliance_list'},
                    {'name': 'Add Appliance', 'url': 'tracker:appliance_create'},
                ]
            },
            {
                'name': 'Electrical',
                'sections': [
                    {
                        'title': 'Circuits',
                        'items': [
                            {'name': 'View All Circuits', 'url': 'tracker:circuit_list'},
                            {'name': 'Add Circuit', 'url': 'tracker:circuit_create'},
                        ]
                    },
                    {
                        'title': 'Diagrams',
                        'items': [
                            {'name': 'View All Diagrams', 'url': 'tracker:circuit_diagram_list'},
                            {'name': 'Add Diagram', 'url': 'tracker:circuit_diagram_create'},
                        ]
                    },
                    {
                        'title': 'Electrical Panels',
                        'items': [
                            {'name': 'View All Panels', 'url': 'tracker:electrical_panel_list'},
                            {'name': 'Add Panel', 'url': 'tracker:electrical_panel_create'},
                        ]
                    },
                    {
                        'title': 'Devices',
                        'items': [
                            {'name': 'View All Devices', 'url': 'tracker:device_list'},
                            {'name': 'Add Device', 'url': 'tracker:device_create'},
                        ]
                    },
                ]
            },
            {
                'name': 'Locations',
                'sections': [
                    {
                        'title': 'Rooms',
                        'items': [
                            {'name': 'View All Rooms', 'url': 'tracker:room_list'},
                            {'name': 'Add Room', 'url': 'tracker:room_create'},
                        ]
                    },
                    {
                        'title': 'Purchase Locations',
                        'items': [
                            {'name': 'View All Purchase Locations', 'url': 'tracker:purchase_location_list'},
                            {'name': 'Add Purchase Location', 'url': 'tracker:purchase_location_create'},
                        ]
                    },
                ]
            },
            {
                'name': 'Paint Colors',
                'items': [
                    {'name': 'View All Paint Colors', 'url': 'tracker:paint_color_list'},
                    {'name': 'Add Paint Color', 'url': 'tracker:paint_color_create'},
                ]
            },
        ],
        'settings_items': [
            {
                'name': 'Data Management',
                'items': [
                    {'name': 'Import/Export Data', 'url': 'tracker:import_export_data'},
                ]
            }
        ]
    }
