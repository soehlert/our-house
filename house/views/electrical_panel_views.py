from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
import logging

from house.models import ElectricalPanel
from house.forms import ElectricalPanelForm
from house.utils import generate_electrical_panel_image_for_panel

logger = logging.getLogger(__name__)


def electrical_panel_list(request):
    """List all electrical panels with search and filtering."""
    panels = ElectricalPanel.objects.prefetch_related('circuits').all()

    search_query = request.GET.get('search', '').strip()
    if search_query:
        panels = panels.filter(
            Q(brand__icontains=search_query) |
            Q(model__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(breaker_type__icontains=search_query) |
            Q(kind__icontains=search_query)
        ).distinct()

    return render(request, 'house/electrical_panels/list.html', {"object_list": panels})


def electrical_panel_detail(request, pk):
    """Display electrical panel details."""
    panel = get_object_or_404(ElectricalPanel.objects.prefetch_related('circuits'), pk=pk)

    # Generate SVG content for this specific panel
    svg_file = generate_electrical_panel_image_for_panel(pk)
    svg_content = svg_file.read().decode('utf-8')

    # Calculate circuit summary stats
    circuits = panel.circuits.all()

    # Count by breaker size
    breaker_counts = {}
    for circuit in circuits:
        breaker_counts[circuit.breaker_size] = breaker_counts.get(circuit.breaker_size, 0) + 1

    protection_counts = {
        'none': circuits.filter(protection_type='none').count(),
        'gfci': circuits.filter(protection_type='gfci').count(),
        'afci': circuits.filter(protection_type='afci').count(),
        'dual_function': circuits.filter(protection_type='dual_function').count(),
    }

    context = {
        'panel': panel,
        'circuits': circuits.order_by('circuit_number'),
        'svg_content': svg_content,
        'breaker_counts': breaker_counts,
        'protection_counts': protection_counts,
    }

    return render(request, 'house/electrical_panels/detail.html', context)


def electrical_panel_create(request):
    """Create a new electrical panel."""
    if request.method == 'POST':
        form = ElectricalPanelForm(request.POST)
        if form.is_valid():
            panel = form.save()
            messages.success(request, f'Electrical panel "{panel.description}" created successfully.')
            if 'save_and_add_another' in request.POST:
                return redirect('house:electrical_panel_create')
            else:
                return redirect('house:electrical_panel_detail', pk=panel.pk)
    else:
        form = ElectricalPanelForm()

    return render(request, 'house/electrical_panels/form.html', {
        'form': form,
        'panel': None
    })


def electrical_panel_update(request, pk):
    """Update an existing electrical panel."""
    panel = get_object_or_404(ElectricalPanel, pk=pk)

    if request.method == 'POST':
        form = ElectricalPanelForm(request.POST, instance=panel)
        if form.is_valid():
            panel = form.save()
            messages.success(request, f'Electrical panel "{panel.description}" updated successfully.')
            return redirect('house:electrical_panel_detail', pk=panel.pk)
    else:
        form = ElectricalPanelForm(instance=panel)

    return render(request, 'house/electrical_panels/form.html', {
        'form': form,
        'panel': panel
    })


def electrical_panel_delete(request, pk):
    """Delete an electrical panel."""
    panel = get_object_or_404(ElectricalPanel, pk=pk)

    if request.method == 'POST':
        panel_info = f"{panel.get_kind_display()} - {panel.description}"
        panel.delete()
        messages.success(request, f'Electrical panel "{panel_info}" deleted successfully.')
        return redirect('house:electrical_panel_list')

    return render(request, 'house/electrical_panels/confirm_delete.html', {
        'panel': panel
    })
