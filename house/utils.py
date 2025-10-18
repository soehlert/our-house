from io import StringIO
from django.core.files.base import ContentFile
from django.conf import settings
import xml.etree.ElementTree as ET
from house.models import Circuit
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
            'empty': '#D1D5DB',              # Gray-300
            'none': '#FEF08A',               # Yellow-200
            'gfci': '#60A5FA',               # Blue-400
            'afci': '#34D399',               # Emerald-400
            'dual_function': '#FB923C',      # Orange-300
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
        from house.models import ElectricalPanel
        try:
            panel = ElectricalPanel.objects.get(id=panel_id)
            circuits = panel.circuits.all()
            return {circuit.circuit_number: circuit for circuit in circuits}
        except ElectricalPanel.DoesNotExist:
            return {}

    @staticmethod
    def _get_panel_title(panel_id: int) -> str:
        """Get the title for a specific panel."""
        from house.models import ElectricalPanel
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
            # Left side positions (moving from outside to center)
            'left_number_x': self.margin + 20,           # Circuit numbers (1, 3, 5)
            'left_label_x': self.margin + 50,            # Circuit descriptions start
            'left_breaker_x': center_x - 90,             # Actual breaker rectangles
            # Right side positions (moving from center to outside)
            'right_breaker_x': center_x + 10,            # Actual breaker rectangles
            'right_label_x': center_x + 110,             # Circuit descriptions start
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
        """Determine what color a breaker should be based on its protection type."""
        if not circuit:
            return self.colors['empty']

        # Map protection_type to colors
        protection_map = {
            'none': self.colors['none'],
            'gfci': self.colors['gfci'],
            'afci': self.colors['afci'],
            'dual_function': self.colors['dual_function']
        }

        return protection_map.get(circuit.protection_type, self.colors['none'])


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

        # Calculate the height for this circuit position
        if circuit_num in double_pole_starts:
            # This is a double-pole breaker
            if side == Side.LEFT:
                next_row_y = layout['start_y'] + ((circuit_num + 1) // 2) * self.row_height
            else:
                next_row_y = layout['start_y'] + (circuit_num // 2) * self.row_height
            breaker_height = next_row_y + self.row_height - y
        else:
            # Single-pole breaker
            breaker_height = self.row_height

        # Position circuit number vertically centered with the breaker
        number_x = layout[f'{side.value}_number_x']
        number_y = y + (breaker_height // 2) + 6  # Center vertically + slight offset for text baseline

        circuit_num_element = ET.SubElement(svg, 'text', {
            'x': str(number_x),
            'y': str(number_y),
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
            # Calculate available width and positioning for text
            if side == Side.LEFT:
                text_start_x = layout['left_number_x'] + 20  # Number position + padding
                text_end_x = layout['left_breaker_x'] - 20  # Breaker position - padding
                available_width = text_end_x - text_start_x
                label_x = text_start_x
                label_class = 'circuit-label'  # Left-aligned
            else:
                # Right side: Breaker → 15px → Text → 15px → Number
                text_start_x = layout['right_breaker_x'] + self.breaker_width + 20  # After breaker + padding
                text_end_x = layout['right_number_x'] - 20   # Before number - padding
                available_width = text_end_x - text_start_x
                label_x = text_start_x
                label_class = 'circuit-label'  # Left-aligned

            # Wrap text to fit available space
            wrapped_lines = self._wrap_text(circuit.description, available_width)

            # Calculate vertical centering
            line_height = 10
            total_text_height = len(wrapped_lines) * line_height

            # Center the text block within the breaker height
            text_start_y = y + (breaker_height - total_text_height) // 2 + 12

            # Draw each line of wrapped text
            for i, line in enumerate(wrapped_lines):
                text_y = text_start_y + (i * line_height)

                ET.SubElement(svg, 'text', {
                    'x': str(label_x),
                    'y': str(text_y),
                    'class': label_class,
                    'fill': '#000000'
                }).text = line

            # Draw breaker size in center of breaker
            breaker_size_y = y + breaker_height // 2 + 4
            ET.SubElement(svg, 'text', {
                'x': str(breaker_x + self.breaker_width // 2),
                'y': str(breaker_size_y),
                'class': 'breaker-size',
                'fill': '#000000'
            }).text = circuit.breaker_size


    def _wrap_text(self, text: str, max_width: int, max_lines: int = 3) -> List[str]:
        """Wrap text to fit within the specified pixel width."""
        if not text:
            return [""]

        # Came to these numbers by sheer brute force
        chars_per_line = max(25, int(max_width / 5.0))

        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + (" " + word if current_line else word)

            if len(test_line) > chars_per_line:
                if current_line:  # If we have content, start a new line
                    lines.append(current_line)
                    current_line = word
                else:
                    lines.append(word)
                    current_line = ""
            else:
                current_line = test_line

        # Add the last line if there's content
        if current_line:
            lines.append(current_line)

        return lines if lines else [""]

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

        # Protection types (updated for new model)
        legend_items = [
            ("Empty Slot", self.colors['empty']),
            ("No Protection", self.colors['none']),
            ("GFCI", self.colors['gfci']),
            ("AFCI", self.colors['afci']),
            ("Dual Function", self.colors['dual_function']),
        ]

        # Draw legend
        for i, (label, color) in enumerate(legend_items):
            col = i % 3
            row = i // 3
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
