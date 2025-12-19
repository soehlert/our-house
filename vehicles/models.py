from django.db import models
from house.models import PurchaseLocation
from .choices import VehicleMakes

class Vehicle(models.Model):
    """Tracks vehicles and their documentation."""
    name = models.CharField(max_length=100)  # e.g., "Dad's Truck"
    make = models.CharField(max_length=25, choices=VehicleMakes.choices)  # e.g., "Ford"
    model = models.CharField(max_length=100) # e.g., "F-150"
    trim = models.CharField(max_length=100, blank=True) # e.g., "Lariat"
    year = models.PositiveIntegerField(null=True, blank=True)
    vin = models.CharField(max_length=17, unique=True, blank=True, null=True)
    license_plate = models.CharField(max_length=10, blank=True)

    # Maintenance Details
    engine_size = models.CharField(max_length=50, blank=True)
    oil_type = models.CharField(max_length=50, blank=True)
    oil_filter_type = models.CharField(max_length=50, blank=True)
    wiper_blade_size_front = models.CharField(max_length=50, blank=True)
    wiper_blade_size_back = models.CharField(max_length=50, blank=True)

    # Documentation
    registration = models.FileField(upload_to="vehicle/registration/", blank=True, null=True)
    insurance = models.FileField(upload_to="vehicle/insurance/", blank=True, null=True)
    service_records = models.FileField(upload_to="vehicle/service/", blank=True, null=True)
    image = models.ImageField(upload_to="vehicle/images/", blank=True, null=True)

    # Purchase info
    purchase_location = models.ForeignKey(
        PurchaseLocation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='vehicles'
    )
    purchase_date = models.DateField(null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Notes
    notes = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.year} {self.make} {self.model}" if self.year and self.make and self.model else self.name