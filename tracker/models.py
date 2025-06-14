from django.db import models
from django.core.exceptions import ValidationError
from .validators import PurchaseLocationValidator

import logging
import hashlib

logger = logging.getLogger(__name__)


class BreakerSize(models.TextChoices):
    FIFTEEN_AMP = "15A", "15A"
    TWENTY_AMP = "20A", "20A"
    THIRTY_AMP = "30A", "30A"
    FORTY_AMP = "40A", "40A"
    FIFTY_AMP = "50A", "50A"
    SIXTY_AMP = "60A", "60A"

class Volts(models.TextChoices):
    ONETWENTY = "120V", "120V"
    TWOFORTY = "240V", "240V"

class PoleType(models.TextChoices):
    SINGLE = "single", "Single Pole"
    DOUBLE = "double", "Double Pole"

class ProtectionType(models.TextChoices):
    """Electrical protection types for circuits and devices."""
    NONE = "none", "No Protection"
    GFCI = "gfci", "GFCI (Ground Fault Circuit Interrupter)"
    AFCI = "afci", "AFCI (Arc Fault Circuit Interrupter)"
    DUAL_FUNCTION = "dual_function", "Dual Function (AFCI + GFCI)"


class Room(models.Model):
    """Represents a room in the house."""
    name = models.CharField(max_length=100, unique=True)
    location_description = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

class PurchaseLocation(models.Model):
    """Stores purchase locations for appliances and other items."""
    name = models.CharField(max_length=100, unique=True)
    website = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def clean(self) -> None:
        """Validate using Pydantic before saving."""
        super().clean()
        print(f"DEBUG: clean() called with website: {self.website}")


        try:
            data = {
                'name': self.name,
                'website': self.website,
                'notes': self.notes,
            }

            validated_data = PurchaseLocationValidator(**data)

            self.name = validated_data.name
            self.website = str(validated_data.website) if validated_data.website else ''

        except Exception as e:
            logger.exception("Validation error for PurchaseLocation")
            raise ValidationError(f"Validation error: {str(e)}")

    def save(self, *args, **kwargs) -> None:
        print(f"DEBUG: save() called with website: {self.website}")

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class ElectricalPanel(models.Model):
    """Define electrical panels."""
    class PanelType(models.TextChoices):
        MAIN = "Main Panel", "Main Panel"
        SUBPANEL = "Subpanel", "Subpanel"
        Disconnect = "Disconnect", "Disconnect"

    brand = models.CharField(max_length=25)
    model = models.CharField(max_length=25, blank=True)
    description = models.TextField(blank=True)
    breaker_type = models.CharField(max_length=25, blank=True)
    kind = models.CharField(max_length=25, choices=PanelType)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.brand} - {self.model}: {self.kind}"


class Appliance(models.Model):
    """Tracks appliances and their documentation."""

    class ApplianceType(models.TextChoices):
        GAS = "gas", "Gas"
        ELECTRIC = "electric", "Electric"
        INDUCTION = "induction", "Induction"
        OTHER = "other", "Other"

    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100, blank=True)
    model_number = models.CharField(max_length=100, blank=True)
    serial_number = models.CharField(max_length=100, blank=True, unique=True)
    appliance_type = models.CharField(
        max_length=10,
        choices=ApplianceType.choices,
        default=ApplianceType.OTHER
    )

    # Dismissable alerts
    warranty_alert_dismissed = models.BooleanField(default=False)
    warranty_alert_dismissed_at = models.DateTimeField(null=True, blank=True)

    # Documentation
    receipt = models.FileField(upload_to="receipts/", blank=True, null=True)
    owners_manual = models.FileField(upload_to="owners_manuals/", blank=True, null=True)
    specs = models.FileField(upload_to="specs/", blank=True, null=True)
    install_docs = models.FileField(upload_to="install_docs/", blank=True, null=True)
    service_manual = models.FileField(upload_to="service_manual/", blank=True, null=True)
    image = models.ImageField(upload_to="appliance_images/", blank=True, null=True)

    # Purchase info
    purchase_location = models.ForeignKey(
        PurchaseLocation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='appliances'
    )
    purchase_date = models.DateField(null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Status
    registered = models.BooleanField(default=False)
    warranty_expires = models.DateField(null=True, blank=True)

    # Technical
    power_demands = models.CharField(max_length=5, blank=True, null=True,
                                     choices=BreakerSize.choices)
    pole_type = models.CharField(max_length=10, blank=True, null=True, choices=PoleType.choices)
    voltage = models.CharField(max_length=10, blank=True, null=True, choices=Volts.choices)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)

    # Notes
    notes = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    @property
    def connected_device(self):
        """Get the device this appliance is connected to."""
        return self.devices.first()

    def __str__(self) -> str:
        return f"{self.name} ({self.model_number})" if self.model_number else self.name


class PaintColor(models.Model):
    """Tracks paint colors used in different rooms."""
    class Finish(models.TextChoices):
        FLAT = "Flat", "Flat"
        MATTE = "Matte", "Matte"
        SATIN ="Satin", "Satin"
        EGGSHELL = "Eggshell", "Eggshell"
        SEMIGLOSS = "Semigloss", "Semigloss"
        GLOSS = "Gloss", "Gloss"

    rooms = models.ManyToManyField(Room, related_name='paint_colors')
    paint_code = models.CharField(max_length=100)
    paint_color = models.CharField(max_length=100)
    paint_brand = models.CharField(max_length=100, blank=True)
    paint_base = models.CharField(max_length=100, blank=True)
    finish_type = models.CharField(max_length=20, blank=True, null=True, choices=Finish.choices)
    purchase_date = models.DateField(null=True, blank=True)
    purchase_location = models.ForeignKey(
        PurchaseLocation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='paint_colors'
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['paint_color']

    def __str__(self) -> str:
        room_names = ", ".join(room.name for room in self.rooms.all()[:3])
        if self.rooms.count() > 3:
            room_names += "..."
        return f"{self.paint_color} - {room_names}"


class CircuitDiagram(models.Model):
    """Electrical circuit diagrams."""
    image = models.ImageField(upload_to="circuit_diagrams/")
    description = models.CharField(max_length=255, blank=True)
    file_hash = models.CharField(max_length=32, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.description or f"Circuit Diagram {self.id}"

    def calculate_hash(self):
        """Calculate and return the hash of the image file."""
        if self.image:
            self.image.seek(0)
            content = self.image.read()
            self.image.seek(0)
            return hashlib.md5(content).hexdigest()
        return ""

    def save(self, *args, **kwargs):
        """Recalculate the hash of the image."""
        self.file_hash = self.calculate_hash()
        super().save(*args, **kwargs)


class Circuit(models.Model):
    """Electrical circuits in the house."""
    rooms = models.ManyToManyField(Room, related_name='circuits')
    circuit_number = models.IntegerField()
    description = models.CharField(max_length=255)

    panel = models.ForeignKey(ElectricalPanel, on_delete=models.CASCADE, related_name='circuits')
    breaker_size = models.CharField(max_length=10, choices=BreakerSize.choices)
    pole_type = models.CharField(max_length=10, choices=PoleType.choices)
    voltage = models.CharField(max_length=10, choices=Volts.choices)
    protection_type = models.CharField(max_length=15, choices=ProtectionType.choices, default=ProtectionType.NONE)

    diagrams = models.ForeignKey(CircuitDiagram, blank=True, null=True, related_name='circuits', on_delete=models.SET_NULL)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['circuit_number']
        unique_together = ['circuit_number']

    def __str__(self) -> str:
        return f"Circuit {self.circuit_number} - {self.description}"


class Device(models.Model):
    """Define electrical devices."""
    class DeviceType(models.TextChoices):
        RECEPTACLE = "Receptacle", "Receptacle"
        SWITCH = "Switch", "Switch"
        LIGHT = "Light", "Light"
        DETECTOR = "Detector", "Detector"
        CEILING_FAN = "Ceiling Fan", "Ceiling Fan"
        FLOOR_HEATING = "Floor Heating", "Floor Heating"

    device_type = models.CharField(max_length=50, choices=DeviceType.choices)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='devices')
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE, blank=True, null=True, related_name='devices')
    location_description = models.TextField(blank=True)
    position_number = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    protection_type = models.CharField(max_length=15, choices=ProtectionType.choices, default=ProtectionType.NONE)
    attached_appliance = models.ForeignKey(Appliance, on_delete=models.CASCADE, null=True, blank=True, related_name='devices')

    class Meta:
        ordering = ['room__name', 'device_type']

    def get_total_protection(self):
        """Get protection features for this device."""
        protection_features = []

        # Only check device-level protection
        if self.protection_type and self.protection_type != ProtectionType.NONE:
            if self.protection_type == ProtectionType.GFCI:
                protection_features.append('GFCI')
            elif self.protection_type == ProtectionType.AFCI:
                protection_features.append('AFCI')
            elif self.protection_type == ProtectionType.DUAL_FUNCTION:
                protection_features.append('GFCI')
                protection_features.append('AFCI')

        return protection_features


    def __str__(self) -> str:
        circuit_info = f"Circuit {self.circuit.circuit_number}" if self.circuit else "No Circuit"
        return f"{self.room.name} - {self.location_description}"
