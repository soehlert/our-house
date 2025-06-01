from django.db import models
from django.core.exceptions import ValidationError
from .validators import PurchaseLocationValidator

import logging

logger = logging.getLogger(__name__)


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


class Appliance(models.Model):
    """Tracks appliances and their documentation."""

    class ApplianceType(models.TextChoices):
        GAS = "gas", "Gas"
        ELECTRIC = "electric", "Electric"
        INDUCTION = "induction", "Induction"
        OTHER = "other", "Other"

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

    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100, blank=True)
    model_number = models.CharField(max_length=100, blank=True)
    serial_number = models.CharField(max_length=100, blank=True, unique=True)
    appliance_type = models.CharField(
        max_length=10,
        choices=ApplianceType.choices,
        default=ApplianceType.OTHER
    )

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

    def __str__(self) -> str:
        return f"{self.name} ({self.model_number})" if self.model_number else self.name


class PaintColor(models.Model):
    """Tracks paint colors used in different rooms."""
    class Finish(models.TextChoices):
        FLAT = "FLAT", "Flat"
        MATTE = "MATTE", "Matte"
        SATIN ="SATIN", "Satin"
        EGGSHELL = "EGGSHELL", "Eggshell"
        SEMIGLOSS = "SEMIGLOSS", "Semigloss"
        GLOSS = "GLOSS", "Gloss"

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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.description or f"Circuit Diagram {self.id}"


class Circuit(models.Model):
    """Electrical circuits in the house."""

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

    rooms = models.ManyToManyField(Room, related_name='circuits')
    circuit_number = models.IntegerField()
    description = models.CharField(max_length=255)

    breaker_size = models.CharField(max_length=10, choices=BreakerSize.choices)
    gfci = models.BooleanField(default=False, verbose_name="GFCI Protected")
    afci = models.BooleanField(default=False, verbose_name="AFCI Protected")
    cafi = models.BooleanField(default=False, verbose_name="CAFI Protected")
    pole_type = models.CharField(max_length=10, choices=PoleType.choices)
    voltage = models.CharField(max_length=10, choices=Volts.choices)

    diagrams = models.ManyToManyField(CircuitDiagram, blank=True, related_name='circuits')
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['circuit_number']
        unique_together = ['circuit_number']

    def __str__(self) -> str:
        return f"Circuit {self.circuit_number} - {self.description}"


class Outlet(models.Model):
    """Define outlets.

    Note: Outlet is the electrician term for any device in the circuit where power goes out. I realize that sounds real
    'akshually' but it's the best description I got here.
    """
    class DeviceType(models.TextChoices):
        RECEPTACLE = "RECEPTACLE", "Receptacle"
        SWITCH = "SWITCH", "Switch"
        LIGHT = "LIGHT", "Light"

    device_type = models.CharField(max_length=50, choices=DeviceType.choices)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='outlets')
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE, related_name='outlets')
    location_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['room__name', 'device_type']

    def __str__(self) -> str:
        return f"{self.get_device_type_display()} in {self.room.name} - Circuit {self.circuit.circuit_number}"
