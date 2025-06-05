from django import forms
from tracker.models import Appliance, Circuit, CircuitDiagram, ElectricalPanel, Outlet, PaintColor, PurchaseLocation, Room


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', "location_description"]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent bg-white shadow-sm',
                'placeholder': 'Human friendly name',
                'data-group': 'details'
            }),
            'location_description': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent bg-white shadow-sm',
                'placeholder': 'Specific location of room',
                'data-group': 'details'
            })
        }
        help_texts = {
            'name': 'Enter a human friendly name for this room',
            'location_description': 'Enter a descriptive name for this room',
        }


class PaintColorForm(forms.ModelForm):
    class Meta:
        model = PaintColor
        fields = [
            'paint_color', 'paint_code', 'paint_brand', 'paint_base',
            'finish_type', 'rooms', 'purchase_date', 'purchase_location', 'notes'
        ]
        widgets = {
            'paint_color': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'data-group': 'details'
            }),
            'paint_code': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'data-group': 'details'
            }),
            'paint_brand': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'data-group': 'details'
            }),
            'paint_base': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'data-group': 'details'
            }),
            'finish_type': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'data-group': 'details'
            }),
            'rooms': forms.CheckboxSelectMultiple(attrs={
                'class': 'space-y-2',
                'data-group': 'relationships'
            }),
            'purchase_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'data-group': 'purchase'
            }),
            'purchase_location': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'data-group': 'purchase'
            }),
            'notes': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'data-group': 'notes'
            }),
        }


class OutletForm(forms.ModelForm):
    class Meta:
        model = Outlet
        fields = ['device_type', 'room', 'circuit', 'location_description', 'position_number', 'protection_type']
        widgets = {
            'device_type': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'data-group': 'details'
            }),
            'room': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'data-group': 'relationships'
            }),
            'circuit': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'data-group': 'relationships'
            }),
            'location_description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'rows': 4,
                'placeholder': 'Where is the outlet located in the room',
                'data-group': 'notes'
            }),
            'position_number': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'Position in circuit',
                'min': '1',
                'data-group': 'details'
            }),
            'protection_type': forms.Select(attrs={  # Added missing widget
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'data-group': 'technical'
            }),
        }
        help_texts = {
            'device_type': 'Select the type of electrical device',
            'room': 'Select the room where this outlet is located',
            'circuit': 'Select the circuit this outlet is connected to',
            'location_description': 'Describe the location of the outlet',
            'position_number': 'eg 1 is the home run, 2 is the next outlet',
            'protection_type': 'Select the type of electrical protection for this outlet',  # Added help text
        }

    def __init__(self, *args, **kwargs):  # Added __init__ method
        super().__init__(*args, **kwargs)
        self.fields['protection_type'].empty_label = "Select protection type"
        self.fields['circuit'].empty_label = "Select circuit"


class PurchaseLocationForm(forms.ModelForm):
    class Meta:
        model = PurchaseLocation
        fields = ['name', 'website', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'e.g., Home Depot, Amazon, Local Hardware Store',
                'data-group': 'details'
            }),
            'website': forms.URLInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'https://example.com',
                'data-group': 'details'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'rows': 4,
                'placeholder': 'Enter any additional notes about this location...',
                'data-group': 'notes'
            }),
        }
        help_texts = {
            'name': 'Enter the name of the store or location',
            'website': 'Optional website URL for this location',
            'notes': 'Any additional information about this purchase location'
        }


class ElectricalPanelForm(forms.ModelForm):
    class Meta:
        model = ElectricalPanel
        fields = [
            'kind', 'brand', 'model', 'description', 'breaker_type'
        ]
        widgets = {
            'kind': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'data-group': 'details'
            }),
            'brand': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'e.g., Square D, Siemens, GE',
                'data-group': 'details'
            }),
            'model': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'Enter model number',
                'data-group': 'details'
            }),
            'description': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'e.g., Main electrical panel, Garage subpanel',
                'data-group': 'details'
            }),
            'breaker_type': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'e.g., QO, Homeline',
                'data-group': 'technical'
            }),
        }
        help_texts = {
            'kind': 'Select the type of electrical panel',
            'brand': 'Enter the manufacturer brand name',
            'model': 'Enter the specific model number of the panel',
            'description': 'Enter a descriptive name for this panel',
            'breaker_type': 'Enter the type of breakers this panel uses'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add empty option for kind selection
        self.fields['kind'].empty_label = "Select panel type"


class CircuitForm(forms.ModelForm):
    class Meta:
        model = Circuit
        fields = [
            'circuit_number', 'description', 'panel', 'breaker_size', 'voltage', 'pole_type',
            'protection_type', 'rooms', 'diagrams', 'notes'  # Added 'panel', replaced protection booleans
        ]
        widgets = {
            'circuit_number': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'e.g., 1, 2, 15',
                'data-group': 'details'
            }),
            'description': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'e.g., Kitchen outlets, Master bedroom lights',
                'data-group': 'details'
            }),
            'panel': forms.Select(attrs={  # Added panel field
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'data-group': 'relationships'
            }),
            'breaker_size': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'data-group': 'technical'
            }),
            'voltage': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'data-group': 'technical'
            }),
            'pole_type': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'data-group': 'technical'
            }),
            'protection_type': forms.Select(attrs={  # Replaced the 3 checkboxes with 1 dropdown
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'data-group': 'technical'
            }),
            'rooms': forms.CheckboxSelectMultiple(attrs={
                'class': 'space-y-2',
                'data-group': 'relationships'
            }),
            'diagrams': forms.CheckboxSelectMultiple(attrs={
                'class': 'space-y-2',
                'data-group': 'relationships'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'rows': 4,
                'placeholder': 'Enter any additional notes about this circuit...',
                'data-group': 'notes'
            }),
        }
        help_texts = {
            'circuit_number': 'Enter the circuit number from your electrical panel',
            'description': 'Brief description of what this circuit powers',
            'panel': 'Select which electrical panel this circuit belongs to',
            'protection_type': 'Select the type of electrical protection for this circuit',
            'rooms': 'Select all rooms this circuit serves',
            'diagrams': 'Select any relevant circuit diagrams'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['voltage'].empty_label = "Select voltage"
        self.fields['panel'].empty_label = "Select panel"
        self.fields['protection_type'].empty_label = "Select protection type"


class CircuitDiagramForm(forms.ModelForm):
    class Meta:
        model = CircuitDiagram
        fields = ['description', 'image']
        widgets = {
            'description': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'e.g., Main panel layout, Kitchen circuit diagram',
                'data-group': 'details'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'accept': 'image/*',
                'data-group': 'files'
            }),
        }
        help_texts = {
            'description': 'Enter a descriptive name for this circuit diagram',
            'image': 'Upload an image file of the circuit diagram'
        }


class ApplianceForm(forms.ModelForm):
    class Meta:
        model = Appliance
        fields = [
            'name', 'brand', 'model_number', 'serial_number', 'appliance_type',
            'room', 'purchase_location', 'purchase_date', 'purchase_price',
            'registered', 'warranty_expires', 'power_demands', 'pole_type', 'voltage',
            'receipt', 'owners_manual', 'specs', 'install_docs', 'service_manual', 'image',
            'notes'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'Enter appliance name',
                'data-group': 'details'
            }),
            'brand': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'Enter brand name',
                'data-group': 'details'
            }),
            'model_number': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'Enter model number',
                'data-group': 'details'
            }),
            'serial_number': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'Enter serial number',
                'data-group': 'details'
            }),
            'appliance_type': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'data-group': 'details'
            }),
            'room': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'data-group': 'relationships'
            }),
            'purchase_location': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'data-group': 'purchase'
            }),
            'purchase_date': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'type': 'date',
                'data-group': 'purchase'
            }),
            'purchase_price': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'step': '0.01',
                'placeholder': '0.00',
                'data-group': 'purchase'
            }),
            'warranty_expires': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'type': 'date',
                'data-group': 'purchase'
            }),
            'power_demands': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'data-group': 'technical'
            }),
            'pole_type': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'data-group': 'technical'
            }),
            'voltage': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'data-group': 'technical'
            }),
            'registered': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded',
                'data-group': 'purchase'
            }),
            'receipt': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'data-group': 'files'
            }),
            'owners_manual': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'data-group': 'files'
            }),
            'specs': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'data-group': 'files'
            }),
            'install_docs': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'data-group': 'files'
            }),
            'service_manual': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'data-group': 'files'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'data-group': 'files'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'rows': 4,
                'placeholder': 'Enter any additional notes...',
                'data-group': 'notes'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add empty option for optional foreign keys
        self.fields['room'].empty_label = "Select a room"
        self.fields['purchase_location'].empty_label = "Select purchase location"
        self.fields['power_demands'].empty_label = "Select power requirement"
