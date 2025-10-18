from django.db import models


class Vehicle(models.Model):
    """Tracks vehicles and their maintenance information."""

    class VehicleType(models.TextChoices):
        CAR = "car", "Car"
        TRUCK = "truck", "Truck"
        SUV = "suv", "SUV"
        MOTORCYCLE = "motorcycle", "Motorcycle"

    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    vin = models.CharField(max_length=17, unique=True)
    vehicle_type = models.CharField(
        max_length=15,
        choices=VehicleType.choices,
        default=VehicleType.CAR
    )

    oil_type = models.CharField(max_length=100, blank=True)
    oil_capacity = models.CharField(max_length=50, blank=True)
    oil_filter_part_number = models.CharField(max_length=100, blank=True)
    air_filter_part_number = models.CharField(max_length=100, blank=True)

    # Last maintenance
    last_oil_change_date = models.DateField(null=True, blank=True)
    last_oil_change_mileage = models.IntegerField(null=True, blank=True)
    current_mileage = models.IntegerField(null=True, blank=True)

    # Documentation
    registration = models.FileField(upload_to="vehicle_docs/registration/", blank=True)
    insurance = models.FileField(upload_to="vehicle_docs/insurance/", blank=True)
    owners_manual = models.FileField(upload_to="vehicle_docs/manuals/", blank=True)
    service_records = models.FileField(upload_to="vehicle_docs/service/", blank=True)
    image = models.ImageField(upload_to="vehicle_images/", blank=True)

    # Notes
    notes = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['year', 'make', 'model']

    def __str__(self) -> str:
        return f"{self.year} {self.make} {self.model}"

    @property
    def miles_since_oil_change(self) -> int | None:
        """Calculate miles since last oil change."""
        if self.current_mileage and self.last_oil_change_mileage:
            return self.current_mileage - self.last_oil_change_mileage
        return None

    @property
    def needs_oil_change(self) -> bool:
        """Check if oil change is due (assuming 5000 mile intervals)."""
        miles_since = self.miles_since_oil_change
        if miles_since is None:
            return False
        return miles_since >= 5000


class TorqueSetting(models.Model):
    """Tracks torque specifications for vehicle components."""

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='torque_settings')
    component = models.CharField(max_length=100)
    torque_value = models.CharField(max_length=50)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['component']
        unique_together = ['vehicle', 'component']

    def __str__(self) -> str:
        return f"{self.vehicle} - {self.component}: {self.torque_value}"


class MaintenanceRecord(models.Model):
    """Tracks maintenance performed on vehicles."""

    class MaintenanceType(models.TextChoices):
        OIL_CHANGE = "oil_change", "Oil Change"
        TIRE_ROTATION = "tire_rotation", "Tire Rotation"
        BRAKE_SERVICE = "brake_service", "Brake Service"
        TRANSMISSION = "transmission", "Transmission Service"
        COOLANT = "coolant", "Coolant Service"
        AIR_FILTER = "air_filter", "Air Filter"
        FUEL_FILTER = "fuel_filter", "Fuel Filter"
        SPARK_PLUGS = "spark_plugs", "Spark Plugs"
        INSPECTION = "inspection", "Inspection"
        OTHER = "other", "Other"

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='maintenance_records')
    maintenance_type = models.CharField(max_length=20, choices=MaintenanceType.choices)
    date_performed = models.DateField()
    mileage = models.IntegerField(null=True, blank=True)
    cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    receipt = models.FileField(upload_to="maintenance_receipts/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_performed']

    def __str__(self) -> str:
        return f"{self.vehicle} - {self.get_maintenance_type_display()} ({self.date_performed})"
