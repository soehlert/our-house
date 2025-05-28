from pydantic import BaseModel, HttpUrl, field_validator, Field
from django.core.exceptions import ValidationError


class PurchaseLocationValidator(BaseModel):
    """Pydantic model for validating PurchaseLocation data."""
    name: str = Field(..., min_length=1, max_length=100)
    website: HttpUrl | None = None
    notes: str | None = None

    @field_validator('website', mode='before')
    def validate_website(cls, v):
        if v and v.startswith('http://'):
            # Convert http to https
            v = v.replace('http://', 'https://')
        elif v and not v.startswith(('http://', 'https://')):
            # Add https if no protocol
            v = f"https://{v}"
        return v

    @field_validator('name')
    def validate_name(cls, v):
        if v.lower() in ['test', 'example', 'placeholder']:
            raise ValueError('Name cannot be a placeholder value')
        return v.title()

    model_config = {'extra': 'ignore'}