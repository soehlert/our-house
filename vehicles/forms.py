from django import forms
from django.urls import reverse_lazy
from .models import Vehicle
from datetime import datetime


class VehicleForm(forms.ModelForm):
    # Dynamically generate year choices from current year down to 1960
    YEAR_CHOICES = [(r, r) for r in range(datetime.now().year + 1, 1959, -1)]
    year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
            'data-group': 'details'
        }),
        initial=datetime.now().year # Set initial year to current year
    )

    class Meta:
        model = Vehicle
        fields = [
            'name', 'make', 'model', 'trim', 'year', 'vin', 'license_plate',
            'engine_size', 'oil_type', 'oil_filter_type', 'wiper_blade_size_front', 'wiper_blade_size_back',
            'purchase_location', 'purchase_date', 'purchase_price',
            'registration', 'insurance', 'service_records', 'image',
            'notes'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'e.g., Dads Truck, The Blue Car',
                'data-group': 'details'
            }),
            'make': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'data-group': 'details',
                'data-model-url': reverse_lazy('vehicles:api_get_vehicle_models', kwargs={'make': 'PLACEHOLDER'})
            }),
            'model': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'e.g., F-150, Camry',
                'data-group': 'details',
                'list': 'model-list'
            }),
            'trim': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'e.g., Lariat, XSE',
                'data-group': 'details'
            }),
            # 'year' widget removed from here as it's defined as a ChoiceField above
            'vin': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'Vehicle Identification Number',
                'data-group': 'details'
            }),
            'license_plate': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'Enter license plate',
                'data-group': 'details'
            }),
            'engine_size': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'e.g., 5.7L V8, 2.0L Turbo',
                'data-group': 'technical'
            }),
            'oil_type': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'e.g., 0W-20 Full Synthetic',
                'data-group': 'technical'
            }),
            'oil_filter_type': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'e.g., PH3600, M1-110A',
                'data-group': 'technical'
            }),
            'wiper_blade_size_front': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'e.g., 22-inch, 24-inch/18-inch',
                'data-group': 'technical'
            }),
            'wiper_blade_size_back': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'e.g., 14-inch',
                'data-group': 'technical'
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
            'registration': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'data-group': 'files'
            }),
            'insurance': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
                'data-group': 'files'
            }),
            'service_records': forms.FileInput(attrs={
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
        self.fields['purchase_location'].empty_label = "Select purchase location"
        self.fields['make'].empty_label = "Select make" # Add empty option for make
