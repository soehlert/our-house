from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q

from house.models import Room
from house.forms import RoomForm


def room_list(request):
    """List all rooms."""
    rooms = Room.objects.all()

    search_query = request.GET.get('search', '').strip()
    if search_query:
        rooms = rooms.filter(
            Q(name__icontains=search_query)
        ).distinct()

    return render(request, 'house/rooms/list.html', {'object_list': rooms})


def room_detail(request, pk):
    """Show room details."""
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'house/rooms/detail.html', {'room': room})


def room_create(request):
    """Create a new room."""
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save()
            messages.success(request, f'Room "{room.name}" created successfully.')
            if 'save_and_add_another' in request.POST:
                return redirect('house:room_create')
            else:
                return redirect('house:room_detail', pk=room.pk)
    else:
        form = RoomForm()

    return render(request, 'house/rooms/form.html', {'form': form})


def room_update(request, pk):
    """Update an existing room."""
    room = get_object_or_404(Room, pk=pk)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            room = form.save()
            messages.success(request, f'Room "{room.name}" updated successfully.')
            return redirect('house:room_detail', pk=room.pk)
    else:
        form = RoomForm(instance=room)

    return render(request, 'house/rooms/form.html', {
        'form': form,
        'object': room
    })



def room_delete(request, pk):
    """Delete a room."""
    room = get_object_or_404(Room, pk=pk)

    if request.method == 'POST':
        room_name = room.name
        room.delete()
        messages.success(request, f'Room "{room_name}" deleted successfully.')
        return redirect('house:room_list')

    return render(request, 'house/rooms/confirm_delete.html', {'room': room})
