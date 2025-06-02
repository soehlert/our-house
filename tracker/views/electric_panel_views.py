from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
import logging

from tracker.models import ElectricPanel
from tracker.forms import ElectricPanelForm

logger = logging.getLogger(__name__)


def electric_panel_list(request):
    """List all electric panels with search and filtering."""
    panels = ElectricPanel.objects.prefetch_related('circuits').all()

    search_query = request.GET.get('search', '').strip()
    if search_query:
        panels = panels.filter(
            Q(brand__icontains=search_query) |
            Q(model__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(breaker_type__icontains=search_query) |
            Q(kind__icontains=search_query)
        ).distinct()

    return render(request, 'tracker/electric_panels/list.html', {"object_list": panels})


def electric_panel_detail(request, pk):
    """Display electric panel details."""
    panel = get_object_or_404(ElectricPanel.objects.prefetch_related('circuits'), pk=pk)

    context = {
        'panel': panel,
        'circuits': panel.circuits.all().order_by('circuit_number'),
    }

    return render(request, 'tracker/electric_panels/detail.html', context)


def electric_panel_create(request):
    """Create a new electric panel."""
    if request.method == 'POST':
        form = ElectricPanelForm(request.POST)
        if form.is_valid():
            panel = form.save()
            messages.success(request, f'Electric panel "{panel.description}" created successfully.')
            if 'save_and_add_another' in request.POST:
                return redirect('tracker:electric_panel_create')
            else:
                return redirect('tracker:electric_panel_detail', pk=panel.pk)
    else:
        form = ElectricPanelForm()

    return render(request, 'tracker/electric_panels/form.html', {
        'form': form,
        'panel': None
    })


def electric_panel_update(request, pk):
    """Update an existing electric panel."""
    panel = get_object_or_404(ElectricPanel, pk=pk)

    if request.method == 'POST':
        form = ElectricPanelForm(request.POST, instance=panel)
        if form.is_valid():
            panel = form.save()
            messages.success(request, f'Electric panel "{panel.description}" updated successfully.')
            return redirect('tracker:electric_panel_detail', pk=panel.pk)
    else:
        form = ElectricPanelForm(instance=panel)

    return render(request, 'tracker/electric_panels/form.html', {
        'form': form,
        'panel': panel
    })


def electric_panel_delete(request, pk):
    """Delete an electric panel."""
    panel = get_object_or_404(ElectricPanel, pk=pk)

    if request.method == 'POST':
        panel_info = f"{panel.get_kind_display()} - {panel.description}"
        panel.delete()
        messages.success(request, f'Electric panel "{panel_info}" deleted successfully.')
        return redirect('tracker:electric_panel_list')

    return render(request, 'tracker/electric_panels/confirm_delete.html', {
        'panel': panel
    })
