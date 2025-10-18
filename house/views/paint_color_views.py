from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q

from house.models import PaintColor, Room
from house.forms import PaintColorForm


def paint_color_list(request):
    """List all paint colors."""
    paint_colors = PaintColor.objects.prefetch_related('rooms').all()

    search_query = request.GET.get('search', '').strip()
    if search_query:
        paint_colors = paint_colors.filter(
            Q(paint_color__icontains=search_query) |
            Q(paint_code__icontains=search_query) |
            Q(paint_brand__icontains=search_query) |
            Q(rooms__name__icontains=search_query) |
            Q(purchase_location__name__icontains=search_query)
        ).distinct()

    return render(request, 'house/paint_colors/list.html', {'object_list': paint_colors})


def paint_color_detail(request, pk):
    """Show paint color details."""
    paint_color = get_object_or_404(PaintColor.objects.prefetch_related('rooms'), pk=pk)
    return render(request, 'house/paint_colors/detail.html', {'paint_color': paint_color})


def paint_color_create(request):
    """Create a new paint color."""
    if request.method == 'POST':
        form = PaintColorForm(request.POST)
        if form.is_valid():
            paint_color = form.save()
            messages.success(request, f'Paint Color "{paint_color.paint_color}" created successfully.')
            if 'save_and_add_another' in request.POST:
                return redirect('house:paint_color_create')
            else:
                return redirect('house:paint_color_detail', pk=paint_color.pk)
    else:
        form = PaintColorForm()

    context = {
        'form': form,
        'title': 'Create Paint Color'
    }
    return render(request, 'house/paint_colors/form.html', context)


def paint_color_update(request, pk):
    """Update an existing paint color."""
    paint_color = get_object_or_404(PaintColor, pk=pk)

    if request.method == 'POST':
        form = PaintColorForm(request.POST, instance=paint_color)
        if form.is_valid():
            paint_color = form.save()
            messages.success(request, f'Paint color "{paint_color.paint_color}" updated successfully.')
            return redirect('house:paint_color_detail', pk=paint_color.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PaintColorForm(instance=paint_color)

    context = {
        'form': form,
        'paint_color': paint_color,
        'title': 'Update Paint Color'
    }
    return render(request, 'house/paint_colors/form.html', context)


def paint_color_delete(request, pk):
    """Delete a paint color."""
    paint_color = get_object_or_404(PaintColor, pk=pk)

    if request.method == 'POST':
        paint_color.delete()
        messages.success(request, f'Paint color "{paint_color.paint_color}" deleted successfully.')
        return redirect('house:paint_color_list')

    return render(request, 'house/paint_colors/confirm_delete.html', {'paint_color': paint_color})
