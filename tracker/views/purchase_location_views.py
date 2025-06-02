from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q

from tracker.models import PurchaseLocation
from tracker.forms import PurchaseLocationForm


def purchase_location_list(request):
    """List all purchase locations."""
    locations = PurchaseLocation.objects.all()

    search_query = request.GET.get('search', '').strip()
    if search_query:
        locations = locations.filter(name__icontains=search_query).distinct()

    return render(request, 'tracker/purchase_locations/list.html', {'object_list': locations})


def purchase_location_detail(request, pk):
    """Show purchase location details."""
    location = get_object_or_404(PurchaseLocation, pk=pk)
    appliances = location.appliances.all()
    return render(request, 'tracker/purchase_locations/detail.html', {
        'location': location,
        'appliances': appliances
    })


def purchase_location_create(request):
    """Create a new purchase location."""
    if request.method == 'POST':
        form = PurchaseLocationForm(request.POST)
        if form.is_valid():
            purchase_location = form.save()
            messages.success(request, f'Purchase location "{purchase_location.name}" created successfully.')
            if 'save_and_add_another' in request.POST:
                return redirect('tracker:purchase_location_create')
            else:
                return redirect('tracker:purchase_location_detail', pk=purchase_location.pk)
    else:
        form = PurchaseLocationForm()

    return render(request, 'tracker/purchase_locations/form.html', {
        'form': form,
        'purchase_location': None
    })


def purchase_location_update(request, pk):
    """Update an existing purchase location."""
    purchase_location = get_object_or_404(PurchaseLocation, pk=pk)

    if request.method == 'POST':
        form = PurchaseLocationForm(request.POST, instance=purchase_location)
        if form.is_valid():
            purchase_location = form.save()
            messages.success(request, f'Purchase location "{purchase_location.name}" updated successfully.')
            return redirect('tracker:purchase_location_detail', pk=purchase_location.pk)
    else:
        form = PurchaseLocationForm(instance=purchase_location)

    return render(request, 'tracker/purchase_locations/form.html', {
        'form': form,
        'location': purchase_location
    })


def purchase_location_delete(request, pk):
    """Delete a purchase location."""
    location = get_object_or_404(PurchaseLocation, pk=pk)

    if request.method == 'POST':
        location_name = location.name
        location.delete()
        messages.success(request, f'Purchase location "{location_name}" deleted successfully.')
        return redirect('purchase_location_list')

    return render(request, 'tracker/purchase_locations/confirm_delete.html', {'location': location})
