from .home_views import home
from .room_views import (
    room_list, room_detail, room_create, room_update, room_delete
)
from .appliance_views import (
    appliance_list, appliance_detail, appliance_create, appliance_update, appliance_delete
)
from .purchase_location_views import (
    purchase_location_list, purchase_location_detail, purchase_location_create, purchase_location_update,
    purchase_location_delete
)
from .paint_color_views import (
    paint_color_list, paint_color_detail, paint_color_create, paint_color_update, paint_color_delete
)
from .circuit_views import (
    circuit_list, circuit_detail, circuit_create, circuit_update, circuit_delete
)

from .circuit_diagram_views import (
    circuit_diagram_list, circuit_diagram_detail, circuit_diagram_create, circuit_diagram_update, circuit_diagram_delete
)

from .device_views import (
    device_list, device_detail, device_create, device_delete, device_update
)

from .electrical_panel_views import (
    electrical_panel_list, electrical_panel_detail, electrical_panel_create, electrical_panel_delete, electrical_panel_update
)

from .import_export_views import (
    import_data, export_data
)
