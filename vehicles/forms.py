from django import forms
from vehicles.models import Vehicle, MaintenanceRecord


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            'make', 'model', 'year', 'vin', 'vehicle_type',
            'oil_type', 'oil_capacity', 'oil_filter_part_number', 'air_filter_part_number',
            'last_oil_change_date', 'last_oil_change_mileage', 'current_mileage',
            'registration', 'insurance', 'owners_manual', 'service_records', 'image',
            'notes'
        ]
        widgets = {
            'make': forms.TextInput(attrs={'class': 'form-input'}),
            'model': forms.TextInput(attrs={'class': 'form-input'}),
            'year': forms.NumberInput(attrs={'class': 'form-input'}),
            'vin': forms.TextInput(attrs={'class': 'form-input'}),
            'vehicle_type': forms.Select(attrs={'class': 'form-select'}),
            'oil_type': forms.TextInput(attrs={'class': 'form-input'}),
            'oil_capacity': forms.TextInput(attrs={'class': 'form-input'}),
            'oil_filter_part_number': forms.TextInput(attrs={'class': 'form-input'}),
            'air_filter_part_number': forms.TextInput(attrs={'class': 'form-input'}),
            'last_oil_change_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'last_oil_change_mileage': forms.NumberInput(attrs={'class': 'form-input'}),
            'current_mileage': forms.NumberInput(attrs={'class': 'form-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
        }


class MaintenanceRecordForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRecord
        fields = [
            'maintenance_type', 'date_performed', 'mileage', 'cost',
            'location', 'description', 'receipt'
        ]
        widgets = {
            'maintenance_type': forms.Select(attrs={'class': 'form-select'}),
            'date_performed': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'mileage': forms.NumberInput(attrs={'class': 'form-input'}),
            'cost': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'location': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
        }
