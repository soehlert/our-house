from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from tracker.models import Appliance, Room, PurchaseLocation
from tracker.forms import ApplianceForm


def appliance_list(request):
    """List all appliances."""
    appliances = Appliance.objects.select_related('room', 'purchase_location').all()
    return render(request, 'tracker/appliances/list.html', {'object_list': appliances})


def appliance_detail(request, pk):
    """Show appliance details."""
    appliance = get_object_or_404(Appliance.objects.select_related('room', 'purchase_location'), pk=pk)
    return render(request, 'tracker/appliances/detail.html', {'appliance': appliance})


def appliance_create(request):
    """Create a new appliance."""
    if request.method == 'POST':
        form = ApplianceForm(request.POST, request.FILES)
        if form.is_valid():
            appliance = form.save()
            messages.success(request, f'Appliance "{appliance.name}" created successfully.')
            if 'save_and_add_another' in request.POST:
                return redirect('tracker:appliance_create')
            else:
                return redirect('tracker:appliance_detail', pk=appliance.pk)
    else:
        form = ApplianceForm()

    return render(request, 'tracker/appliances/form.html', {'form': form})


def appliance_update(request, pk):
    """Update an existing appliance."""
    appliance = get_object_or_404(Appliance, pk=pk)

    if request.method == 'POST':
        form = ApplianceForm(request.POST, request.FILES, instance=appliance)
        if form.is_valid():
            appliance = form.save()
            messages.success(request, f'Appliance "{appliance.name}" updated successfully.')
            return redirect('tracker:appliance_detail', pk=appliance.pk)
    else:
        form = ApplianceForm(instance=appliance)

    return render(request, 'tracker/appliances/form.html', {
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
        return redirect('tracker:appliance_list')

    return render(request, 'tracker/appliances/confirm_delete.html', {'appliance': appliance})
