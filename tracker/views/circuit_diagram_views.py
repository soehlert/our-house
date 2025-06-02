from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q

from tracker.models import CircuitDiagram
from tracker.forms import CircuitDiagramForm


def circuit_diagram_list(request):
    """List all circuit diagrams."""
    diagrams = CircuitDiagram.objects.all()

    search_query = request.GET.get('search', '').strip()
    if search_query:
        diagrams = diagrams.filter(
            Q(description__icontains=search_query)
        ).distinct()

    return render(request, 'tracker/circuit_diagrams/list.html', {'object_list': diagrams})


def circuit_diagram_detail(request, pk):
    """Show circuit diagram details."""
    diagram = get_object_or_404(CircuitDiagram, pk=pk)
    circuits = diagram.circuits.all()
    return render(request, 'tracker/circuit_diagrams/detail.html', {
        'diagram': diagram,
        'circuits': circuits
    })


def circuit_diagram_create(request):
    """Create a new circuit diagram."""
    if request.method == 'POST':
        form = CircuitDiagramForm(request.POST)
        if form.is_valid():
            circuit_diagram = form.save()
            messages.success(request, f'Circuit diagram "{circuit_diagram.description}" created successfully.')
            if 'save_and_add_another' in request.POST:
                return redirect('tracker:circuit_diagram_create')
            else:
                return redirect('tracker:circuit_diagram_detail', pk=circuit_diagram.pk)
    else:
        form = CircuitDiagramForm()

    return render(request, 'tracker/circuit_diagrams/form.html', {
        'form': form,
        'circuit_diagram': None
    })


def circuit_diagram_update(request, pk):
    """Update an existing circuit diagram."""
    circuit_diagram = get_object_or_404(CircuitDiagram, pk=pk)

    if request.method == 'POST':
        form = CircuitDiagramForm(request.POST, request.FILES, instance=circuit_diagram)
        if form.is_valid():
            circuit_diagram = form.save()
            messages.success(request, f'Circuit diagram "{circuit_diagram}" updated successfully.')
            return redirect('tracker:circuit_diagram_detail', pk=circuit_diagram.pk)
    else:
        form = CircuitDiagramForm(instance=circuit_diagram)

    return render(request, 'tracker/circuit_diagrams/form.html', {
        'form': form,
        'circuit_diagram': circuit_diagram
    })


def circuit_diagram_delete(request, pk):
    """Delete a circuit diagram."""
    diagram = get_object_or_404(CircuitDiagram, pk=pk)

    if request.method == 'POST':
        diagram.delete()
        messages.success(request, f'Circuit diagram deleted successfully.')
        return redirect('tracker:circuit_diagram_list')

    return render(request, 'tracker/circuit_diagrams/confirm_delete.html', {'diagram': diagram})
