from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ..models import Circuit, Room, CircuitDiagram


def circuit_list(request):
    """List all circuits."""
    circuits = Circuit.objects.prefetch_related('rooms', 'diagrams').all()
    return render(request, 'tracker/circuits/list.html', {'circuits': circuits})


def circuit_detail(request, pk):
    """Show circuit details."""
    circuit = get_object_or_404(Circuit.objects.prefetch_related('rooms', 'diagrams'), pk=pk)
    return render(request, 'tracker/circuits/detail.html', {'circuit': circuit})


def circuit_create(request):
    """Create a new circuit."""
    if request.method == 'POST':
        try:
            circuit = Circuit.objects.create(
                circuit_number=request.POST.get('circuit_number'),
                description=request.POST.get('description'),
                breaker_size=request.POST.get('breaker_size'),
                gfci=bool(request.POST.get('gfci')),
                afci=bool(request.POST.get('afci')),
                cafi=bool(request.POST.get('cafi')),
                pole_type=request.POST.get('pole_type'),
                voltage=request.POST.get('voltage', ''),
                notes=request.POST.get('notes', '')
            )

            # Handle many-to-many relationships
            room_ids = request.POST.getlist('rooms')
            if room_ids:
                circuit.rooms.set(room_ids)

            diagram_ids = request.POST.getlist('diagrams')
            if diagram_ids:
                circuit.diagrams.set(diagram_ids)

            messages.success(request, f'Circuit {circuit.circuit_number} created successfully.')
            return redirect('circuit_detail', pk=circuit.pk)
        except Exception as e:
            messages.error(request, f'Error creating circuit: {str(e)}')

    context = {
        'rooms': Room.objects.all(),
        'diagrams': CircuitDiagram.objects.all(),
        'breaker_sizes': Circuit.BreakerSize.choices,
        'pole_types': Circuit.PoleType.choices,
        'voltages': Circuit.Volts.choices,
        'title': 'Create Circuit'
    }
    return render(request, 'tracker/circuits/form.html', context)


def circuit_update(request, pk):
    """Update an existing circuit."""
    circuit = get_object_or_404(Circuit, pk=pk)

    if request.method == 'POST':
        try:
            circuit.circuit_number = request.POST.get('circuit_number')
            circuit.description = request.POST.get('description')
            circuit.breaker_size = request.POST.get('breaker_size')
            circuit.gfci = bool(request.POST.get('gfci'))
            circuit.afci = bool(request.POST.get('afci'))
            circuit.cafi = bool(request.POST.get('cafi'))
            circuit.pole_type = request.POST.get('pole_type')
            circuit.voltage = request.POST.get('voltage', '')
            circuit.notes = request.POST.get('notes', '')
            circuit.save()

            # Handle many-to-many relationships
            room_ids = request.POST.getlist('rooms')
            circuit.rooms.set(room_ids)

            diagram_ids = request.POST.getlist('diagrams')
            circuit.diagrams.set(diagram_ids)

            messages.success(request, f'Circuit {circuit.circuit_number} updated successfully.')
            return redirect('circuit_detail', pk=circuit.pk)
        except Exception as e:
            messages.error(request, f'Error updating circuit: {str(e)}')

    context = {
        'circuit': circuit,
        'rooms': Room.objects.all(),
        'diagrams': CircuitDiagram.objects.all(),
        'breaker_sizes': Circuit.BreakerSize.choices,
        'pole_types': Circuit.PoleType.choices,
        'voltages': Circuit.Volts.choices,
        'title': 'Update Circuit'
    }
    return render(request, 'tracker/circuits/form.html', context)


def circuit_delete(request, pk):
    """Delete a circuit."""
    circuit = get_object_or_404(Circuit, pk=pk)

    if request.method == 'POST':
        circuit_number = circuit.circuit_number
        circuit.delete()
        messages.success(request, f'Circuit {circuit_number} deleted successfully.')
        return redirect('circuit_list')

    return render(request, 'tracker/circuits/confirm_delete.html', {'circuit': circuit})
