from io import StringIO
from django.core.files.base import ContentFile
from django.conf import settings
import xml.etree.ElementTree as ET
from tracker.models import Circuit
from typing import Dict, Set, Tuple, List
from enum import Enum


class Side(Enum):
    LEFT = "left"
    RIGHT = "right"


class ElectricalPanelGenerator:
    """Generates SVG representations of electrical panels."""

    def __init__(self):
        # Color scheme for different protection types
        self.colors = {
            'empty': '#DCDCDC',              # Light gray - empty slot
            'no_protection': '#E6F3FF',      # Very light blue - circuit with no protection
            'gfci': '#96C8FF',               # Light blue - GFCI
            'afci': '#FFC896',               # Light orange - AFCI
            'cafi': '#C8FF96',               # Light green - CAFI
            'gfci_afci': '#C896FF',          # Light purple - GFCI + AFCI
            'gfci_cafi': '#96FFC8',          # Light teal - GFCI + CAFI
            'afci_cafi': '#FFFF96',          # Light yellow - AFCI + CAFI
            'all_three': '#FFB4B4',          # Light pink - All three
        }

        # Layout constants - these define the physical dimensions of the panel inside the SVG
        self.width = 900
        self.row_height = 30
        self.margin = 60
        self.breaker_width = 80
        self.legend_height = 100

    def generate_panel_image(self) -> ContentFile:
        """Coordinate the actual SVG generation process for all circuits."""
        circuits = self._get_circuit_data()
        dimensions = self._calculate_dimensions(circuits)

        # Create the basic SVG structure
        svg = self._create_svg_root(dimensions)
        self._add_styles(svg)
        self._add_title(svg, "Electrical Panel")
        layout = self._calculate_layout()
        self._draw_panel_structure(svg, layout, dimensions)
        double_pole_info = self._analyze_double_pole_breakers(circuits)
        self._draw_all_circuits(svg, circuits, layout, dimensions, double_pole_info)
        self._draw_legend(svg, dimensions)

        return self._convert_to_file(svg)

    def generate_panel_image_for_panel(self, panel_id: int) -> ContentFile:
        """Generate SVG for a specific electrical panel."""
        circuits = self._get_circuit_data_for_panel(panel_id)
        panel_title = self._get_panel_title(panel_id)
        dimensions = self._calculate_dimensions(circuits)

        # Create the basic SVG structure
        svg = self._create_svg_root(dimensions)
        self._add_styles(svg)
        self._add_title(svg, panel_title)
        layout = self._calculate_layout()
        self._draw_panel_structure(svg, layout, dimensions)
        double_pole_info = self._analyze_double_pole_breakers(circuits)
        self._draw_all_circuits(svg, circuits, layout, dimensions, double_pole_info)
        self._draw_legend(svg, dimensions)

        return self._convert_to_file(svg)

    @staticmethod
    def _get_circuit_data() -> Dict[int, Circuit]:
        """Fetch all circuits from database and organizes them by circuit number."""
        circuits = Circuit.objects.all()
        return {circuit.circuit_number: circuit for circuit in circuits}

    @staticmethod
    def _get_circuit_data_for_panel(panel_id: int) -> Dict[int, Circuit]:
        """Fetch circuits for a specific panel."""
        from tracker.models import ElectricalPanel
        try:
            panel = ElectricalPanel.objects.get(id=panel_id)
            circuits = panel.circuits.all()
            return {circuit.circuit_number: circuit for circuit in circuits}
        except ElectricalPanel.DoesNotExist:
            return {}

    @staticmethod
    def _get_panel_title(panel_id: int) -> str:
        """Get the title for a specific panel."""
        from tracker.models import ElectricalPanel
        try:
            panel = ElectricalPanel.objects.get(id=panel_id)
            if panel.description:
                return panel.description
            else:
                return f"{panel.kind} - {panel.brand}"
        except ElectricalPanel.DoesNotExist:
            return "Electrical Panel"

    def _calculate_dimensions(self, circuits: Dict[int, Circuit]) -> Dict[str, int]:
        """Figure out how big the SVG needs to be based on the highest circuit number."""
        if not circuits:
            max_circuit = 4
        else:
            max_circuit = max(circuits.keys())

            for circuit_num, circuit in circuits.items():
                if circuit.pole_type == 'double':
                    effective_max = circuit_num + 2
                    max_circuit = max(max_circuit, effective_max)

        # Ensure we show complete rows
        if max_circuit % 2 == 1:
            max_circuit += 1

        # Calculate actual space needed
        rows_needed = max_circuit // 2
        panel_height = rows_needed * self.row_height
        total_height = 80 + panel_height + self.legend_height + 40

        return {
            'width': self.width,
            'height': total_height,
            'panel_height': panel_height,
            'legend_height': self.legend_height,
            'max_circuit': max_circuit,
            'rows_needed': rows_needed
        }

    @staticmethod
    def _create_svg_root(dimensions: Dict[str, int]) -> ET.Element:
        """Create the root <svg> element with proper dimensions and viewBox."""
        return ET.Element('svg', {
            'width': str(dimensions['width']),
            'height': str(dimensions['height']),
            'viewBox': f"0 0 {dimensions['width']} {dimensions['height']}",
            'xmlns': 'http://www.w3.org/2000/svg'
        })

    @staticmethod
    def _add_styles(svg: ET.Element) -> None:
        """Add CSS styles to the SVG for consistent text formatting and responsive behavior."""
        style = ET.SubElement(svg, 'style')
        style.text = """
            .panel-title { font-family: Arial, sans-serif; font-size: 16px; font-weight: bold; text-anchor: middle; }
            .circuit-number { font-family: Arial, sans-serif; font-size: 10px; text-anchor: middle; }
            .circuit-label { font-family: Arial, sans-serif; font-size: 11px; }
            .circuit-label-right { font-family: Arial, sans-serif; font-size: 11px; text-anchor: end; }
            .breaker-size { font-family: Arial, sans-serif; font-size: 10px; text-anchor: middle; }
            .legend-title { font-family: Arial, sans-serif; font-size: 11px; font-weight: bold; }
            .legend-text { font-family: Arial, sans-serif; font-size: 9px; }
            .panel-border { fill: none; stroke: #646464; stroke-width: 2; }
            .center-line { stroke: #646464; stroke-width: 2; }
            .breaker { stroke: #646464; stroke-width: 1; }
            @media (max-width: 768px) { svg { max-width: 100%; height: auto; } }
        """

    def _add_title(self, svg: ET.Element, title_text: str) -> None:
        """Add title at the top center of the diagram."""
        title = ET.SubElement(svg, 'text', {
            'x': str(self.width // 2),
            'y': '30',
            'class': 'panel-title',
            'fill': '#000000'
        })
        title.text = title_text

    def _calculate_layout(self) -> Dict[str, int]:
        """
        Calculates the X and Y positions for all the different elements.
        This creates the layout: Numbers | Labels | Breakers | Center | Breakers | Labels | Numbers
        """
        center_x = self.width // 2

        return {
            'start_y': 60,
            'center_x': center_x,
            # Left side positions (moving from outside toward center)
            'left_number_x': self.margin + 20,      # Circuit numbers (1, 3, 5)
            'left_label_x': self.margin + 50,       # Circuit descriptions
            'left_breaker_x': center_x - 90,        # Actual breaker rectangles
            # Right side positions (moving from center toward outside)
            'right_breaker_x': center_x + 10,       # Actual breaker rectangles
            'right_label_x': self.width - self.margin - 50,  # Circuit descriptions
            'right_number_x': self.width - self.margin - 20, # Circuit numbers (2, 4, 6)
        }

    def _draw_panel_structure(self, svg: ET.Element, layout: Dict[str, int], dimensions: Dict[str, int]) -> None:
        """Draw the basic panel structure: the outer border and the center dividing line."""
        # Draw the outer border of the panel
        ET.SubElement(svg, 'rect', {
            'x': str(self.margin),
            'y': str(layout['start_y'] - 10),
            'width': str(self.width - 2 * self.margin),
            'height': str(dimensions['panel_height'] + 20),
            'class': 'panel-border'
        })

        # Draw the center dividing line that separates odd/even circuits
        ET.SubElement(svg, 'line', {
            'x1': str(layout['center_x']),
            'y1': str(layout['start_y']),
            'x2': str(layout['center_x']),
            'y2': str(layout['start_y'] + dimensions['panel_height']),
            'class': 'center-line'
        })

    def _get_protection_color(self, circuit: Circuit | None) -> str:
        """Determine what color a breaker should be based on its protection features."""
        if not circuit:
            return self.colors['empty']

        # Use the same logic as the original function
        if circuit.gfci and circuit.afci and circuit.cafi:
            return self.colors['all_three']
        elif circuit.gfci and circuit.afci:
            return self.colors['gfci_afci']
        elif circuit.gfci and circuit.cafi:
            return self.colors['gfci_cafi']
        elif circuit.afci and circuit.cafi:
            return self.colors['afci_cafi']
        elif circuit.gfci:
            return self.colors['gfci']
        elif circuit.afci:
            return self.colors['afci']
        elif circuit.cafi:
            return self.colors['cafi']
        else:
            return self.colors['no_protection']

    @staticmethod
    def _analyze_double_pole_breakers(circuits: dict[int, Circuit]) -> tuple[Set[int], dict[int, Circuit]]:
        """
        Identifies double-pole breakers and marks which positions they occupy.
        Double-pole breakers take up two adjacent positions (e.g., positions 1 and 3, or 2 and 4).

        Returns:
        - used_positions: Set of all positions occupied by double-pole breakers
        - double_pole_starts: Dict mapping starting position to the circuit object
        """
        used_positions = set()
        double_pole_starts = {}

        for circuit_num, circuit in circuits.items():
            if circuit.pole_type == 'double':
                # Mark this as the start of a double-pole breaker
                double_pole_starts[circuit_num] = circuit
                # Mark both positions as used (current + 2 positions down)
                used_positions.add(circuit_num)
                used_positions.add(circuit_num + 2)

        return used_positions, double_pole_starts

    def _draw_all_circuits(self, svg: ET.Element, circuits: Dict[int, Circuit],
                           layout: Dict[str, int], dimensions: Dict[str, int],
                           double_pole_info: Tuple[Set[int], Dict[int, Circuit]]) -> None:
        """Orchestrate drawing all circuit positions from 1 to max_circuit."""
        used_positions, double_pole_starts = double_pole_info

        for i in range(1, dimensions['max_circuit'] + 1):
            side = Side.LEFT if i % 2 == 1 else Side.RIGHT
            self._draw_circuit(svg, i, circuits, layout, used_positions, double_pole_starts, side)

    def _draw_circuit(self, svg: ET.Element, circuit_num: int, circuits: Dict[int, Circuit],
                      layout: Dict[str, int], used_positions: Set[int],
                      double_pole_starts: Dict[int, Circuit], side: Side) -> None:
        """Draw a single circuit position on either side of the panel."""
        if side == Side.LEFT:
            row = (circuit_num - 1) // 2
        else:
            row = (circuit_num - 2) // 2

        y = layout['start_y'] + row * self.row_height
        circuit = circuits.get(circuit_num)

        number_x = layout[f'{side.value}_number_x']
        circuit_num_element = ET.SubElement(svg, 'text', {
            'x': str(number_x),
            'y': str(y + 18),
            'class': 'circuit-number',
            'fill': '#000000'
        })
        circuit_num_element.text = str(circuit_num)

        if circuit_num in double_pole_starts:
            self._draw_breaker(svg, double_pole_starts[circuit_num], circuit_num, layout, y, side, is_double_pole=True)
        elif circuit_num not in used_positions:
            self._draw_breaker(svg, circuit, circuit_num, layout, y, side, is_double_pole=False)

    def _draw_breaker(self, svg: ET.Element, circuit: Circuit | None, circuit_num: int,
                      layout: Dict[str, int], y: int, side: Side, is_double_pole: bool = False) -> None:
        """Draws a breaker (single or double-pole) on the specified side."""
        breaker_color = self._get_protection_color(circuit)

        # Calculate breaker height
        if is_double_pole:
            if side == Side.LEFT:
                next_row_y = layout['start_y'] + ((circuit_num + 1) // 2) * self.row_height
            else:
                next_row_y = layout['start_y'] + (circuit_num // 2) * self.row_height
            breaker_height = next_row_y + self.row_height - y
        else:
            breaker_height = self.row_height

        # Get side-specific coordinates
        breaker_x = layout[f'{side.value}_breaker_x']
        label_x = layout[f'{side.value}_label_x']
        label_class = 'circuit-label' if side == Side.LEFT else 'circuit-label-right'

        # Draw the breaker rectangle
        ET.SubElement(svg, 'rect', {
            'x': str(breaker_x),
            'y': str(y),
            'width': str(self.breaker_width),
            'height': str(breaker_height),
            'fill': breaker_color,
            'class': 'breaker'
        })

        if circuit:
            description = circuit.description[:45] + "..." if len(circuit.description) > 45 else circuit.description

            # Position text differently for single vs double-pole
            if is_double_pole:
                text_y = y + self.row_height  # Center vertically in double-height space
                breaker_size_y = y + breaker_height // 2 + 5  # Center of breaker
            else:
                text_y = y + 18  # Standard single-pole position
                breaker_size_y = y + 18  # Standard single-pole position

            ET.SubElement(svg, 'text', {
                'x': str(label_x),
                'y': str(text_y),
                'class': label_class,
                'fill': '#000000'
            }).text = description

            # Draw breaker size in center of breaker
            ET.SubElement(svg, 'text', {
                'x': str(breaker_x + self.breaker_width // 2),
                'y': str(breaker_size_y),
                'class': 'breaker-size',
                'fill': '#000000'
            }).text = circuit.breaker_size

    def _draw_legend(self, svg: ET.Element, dimensions: Dict[str, int]) -> None:
        """Draw the color legend at the bottom of the panel."""
        legend_y = 60 + dimensions['panel_height'] + 30

        # Legend title
        ET.SubElement(svg, 'text', {
            'x': str(self.margin),
            'y': str(legend_y),
            'class': 'legend-title',
            'fill': '#000000'
        }).text = 'Protection Types:'

        # Protection combinations
        legend_items = [
            ("Empty Slot", self.colors['empty']),
            ("No Protection", self.colors['no_protection']),
            ("GFCI", self.colors['gfci']),
            ("AFCI", self.colors['afci']),
            ("CAFI", self.colors['cafi']),
            ("GFCI + AFCI", self.colors['gfci_afci']),
            ("GFCI + CAFI", self.colors['gfci_cafi']),
            ("AFCI + CAFI", self.colors['afci_cafi']),
            ("All Three", self.colors['all_three']),
        ]

        # Draw legend
        for i, (label, color) in enumerate(legend_items):
            col = i % 2
            row = i // 2
            x = self.margin + col * 200
            y = legend_y + 20 + row * 20

            # Draw colored square
            ET.SubElement(svg, 'rect', {
                'x': str(x),
                'y': str(y),
                'width': '15',
                'height': '15',
                'fill': color,
                'stroke': '#646464',
                'stroke-width': '1'
            })

            # Draw label text next to the square
            ET.SubElement(svg, 'text', {
                'x': str(x + 20),
                'y': str(y + 12),
                'class': 'legend-text',
                'fill': '#000000'
            }).text = label

    @staticmethod
    def _convert_to_file(svg: ET.Element) -> ContentFile:
        """Convert the completed SVG element tree into a ContentFile that Django can serve."""
        svg_string = ET.tostring(svg, encoding='unicode')
        svg_content = f'<?xml version="1.0" encoding="UTF-8"?>\n{svg_string}'
        return ContentFile(svg_content.encode('utf-8'), name='electrical_panel.svg')


def generate_electrical_panel_image_for_panel(panel_id: int) -> ContentFile:
    """Generate SVG for a specific electrical panel."""
    generator = ElectricalPanelGenerator()
    return generator.generate_panel_image_for_panel(panel_id)
