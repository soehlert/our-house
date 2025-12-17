from django import template
from collections import defaultdict

from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def group_fields(form):
    """Group form fields by their data-group attribute."""
    groups = defaultdict(list)

    # Get data groups per form field
    for field in form:
        group = field.field.widget.attrs.get('data-group', 'details')
        groups[group].append(field)

    ordered_groups = []
    group_order = ['details', 'relationships', 'purchase', 'technical', 'files', 'notes']

    for group_name in group_order:
        if group_name in groups:
            ordered_groups.append({
                'name': group_name,
                'fields': groups[group_name]
            })

    for group_name, fields in groups.items():
        if group_name not in group_order:
            ordered_groups.append({
                'name': group_name,
                'fields': fields
            })

    return ordered_groups

@register.filter
@stringfilter
def group_title(group_name):
    """Convert group name to display title."""
    titles = {
        'details': 'Details',
        'relationships': 'Relationships',
        'purchase': 'Purchase Information',
        'technical': 'Technical Information',
        'files': 'Documentation',
        'notes': 'Notes'
    }
    return titles.get(group_name, group_name.title())
