from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q

from house.models import Appliance, Room, PurchaseLocation
from house.forms import ApplianceForm


def appliance_list(request):
    """List all appliances."""
    appliances = Appliance.objects.select_related('room', 'purchase_location').all()

    search_query = request.GET.get('search', '').strip()
    if search_query:
        appliances = appliances.filter(
            Q(name__icontains=search_query) |
            Q(brand__icontains=search_query) |
            Q(model_number__icontains=search_query) |
            Q(serial_number__icontains=search_query) |
            Q(room__name__icontains=search_query) |
            Q(purchase_location__name__icontains=search_query)
        ).distinct()

    return render(request, 'house/appliances/list.html', {'object_list': appliances})


def appliance_detail(request, pk):
    """Show appliance details."""
    appliance = get_object_or_404(Appliance.objects.select_related('room', 'purchase_location'), pk=pk)
    return render(request, 'house/appliances/detail.html', {'appliance': appliance})


def appliance_create(request):
    """Create a new appliance."""
    if request.method == 'POST':
        form = ApplianceForm(request.POST, request.FILES)
        if form.is_valid():
            appliance = form.save()
            messages.success(request, f'Appliance "{appliance.name}" created successfully.')
            if 'save_and_add_another' in request.POST:
                return redirect('house:appliance_create')
            else:
                return redirect('house:appliance_detail', pk=appliance.pk)
    else:
        form = ApplianceForm()

    return render(request, 'house/appliances/form.html', {'form': form})


def appliance_update(request, pk):
    """Update an existing appliance."""
    appliance = get_object_or_404(Appliance, pk=pk)

    if request.method == 'POST':
        form = ApplianceForm(request.POST, request.FILES, instance=appliance)
        if form.is_valid():
            appliance = form.save()
            messages.success(request, f'Appliance "{appliance.name}" updated successfully.')
            return redirect('house:appliance_detail', pk=appliance.pk)
    else:
        form = ApplianceForm(instance=appliance)

    return render(request, 'house/appliances/form.html', {
        'form': form,
        'appliance': appliance
    })


def appliance_delete(request, pk):
    """Delete an appliance."""
    appliance = get_object_or_404(Appliance, pk=pk)

    if request.method == 'POST':
        appliance_name = appliance.name
        appliance.delete()
        messages.success(request, f'Appliance "{appliance_name}" deleted successfully.')
        return redirect('house:appliance_list')

    return render(request, 'house/appliances/confirm_delete.html', {'appliance': appliance})
