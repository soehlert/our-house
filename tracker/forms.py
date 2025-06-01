from django import forms
from tracker.models import Appliance, Circuit, CircuitDiagram, Outlet, PaintColor, PurchaseLocation, Room


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
        fields = ['device_type', 'room', 'circuit', 'location_description']
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
        }
        help_texts = {
            'device_type': 'Select the type of electrical device',
            'room': 'Select the room where this outlet is located',
            'circuit': 'Select the circuit this outlet is connected to',
            'location_description': 'Describe the location of the outlet',
        }


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


class CircuitForm(forms.ModelForm):
    class Meta:
        model = Circuit
        fields = [
            'circuit_number', 'description', 'breaker_size', 'voltage', 'pole_type',
            'gfci', 'afci', 'cafi', 'rooms', 'diagrams', 'notes'
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
            'gfci': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded',
                'data-group': 'technical'
            }),
            'afci': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded',
                'data-group': 'technical'
            }),
            'cafi': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded',
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
            'rooms': 'Select all rooms this circuit serves',
            'diagrams': 'Select any relevant circuit diagrams'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['voltage'].empty_label = "Select voltage"


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
