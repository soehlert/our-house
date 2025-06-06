from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from tracker.models import Circuit, Room, CircuitDiagram
from tracker.forms import CircuitForm


def circuit_list(request):
    """List all circuits."""
    # Handle search
    circuits = Circuit.objects.prefetch_related('rooms', 'diagrams').all()

    search_query = request.GET.get('search', '').strip()
    if search_query:
        circuits = circuits.filter(
            Q(description__icontains=search_query) |
            Q(circuit_number__icontains=search_query) |
            Q(rooms__name__icontains=search_query)
        ).distinct()

    return render(request, 'tracker/circuits/list.html', {'object_list': circuits})


def circuit_detail(request, pk):
    """Show circuit details."""
    circuit = get_object_or_404(Circuit.objects.prefetch_related('rooms', 'diagrams', 'devices'), pk=pk)
    return render(request, 'tracker/circuits/detail.html', {'circuit': circuit})


def circuit_create(request):
    """Create a new circuit."""
    if request.method == 'POST':
        form = CircuitForm(request.POST, request.FILES)
        if form.is_valid():
            circuit = form.save()
            messages.success(request, f'Circuit "{circuit.description}" created successfully.')
            if 'save_and_add_another' in request.POST:
                return redirect('tracker:circuit_create')
            else:
                return redirect('tracker:circuit_detail', pk=circuit.pk)
    else:
        form = CircuitForm()

    return render(request, 'tracker/circuits/form.html', {
        'form': form,
        'circuit': None
    })


def circuit_update(request, pk):
    """Update an existing circuit."""
    circuit = get_object_or_404(Circuit, pk=pk)

    if request.method == 'POST':
        form = CircuitForm(request.POST, request.FILES, instance=circuit)
        if form.is_valid():
            circuit = form.save()
            messages.success(request, f'Circuit {circuit.circuit_number} updated successfully.')
            return redirect('tracker:circuit_detail', pk=circuit.pk)
    else:
        form = CircuitForm(instance=circuit)

    return render(request, 'tracker/circuits/form.html', {
        'form': form,
        'circuit': circuit
    })


def circuit_delete(request, pk):
    """Delete a circuit."""
    circuit = get_object_or_404(Circuit, pk=pk)

    if request.method == 'POST':
        circuit_number = circuit.circuit_number
        circuit.delete()
        messages.success(request, f'Circuit {circuit_number} deleted successfully.')
        return redirect('tracker:circuit_list')

    return render(request, 'tracker/circuits/confirm_delete.html', {'circuit': circuit})
