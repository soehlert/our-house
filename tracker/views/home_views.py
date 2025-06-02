from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from django.shortcuts import render
from django.apps import apps
from django.http import HttpResponse

from tracker.models import Room, Appliance, PurchaseLocation, PaintColor, Circuit, Outlet


def _get_warranty_data():
    """Helper function to get warranty expiration data."""
    today = timezone.now().date()

    expired_appliances = Appliance.objects.filter(
        warranty_expires__lt=today,
        warranty_expires__isnull=False
    ).order_by('warranty_expires')

    expiring_appliances = Appliance.objects.filter(
        warranty_expires__gte=today,
        warranty_expires__lte=today + timedelta(days=90)
    ).order_by('warranty_expires')

    return {
        'expired_appliances': expired_appliances,
        'expiring_appliances': expiring_appliances,
        'total_count': expired_appliances.count() + expiring_appliances.count(),
    }

def home(request):
    """Home page showing overview of all data."""

    # Expiring warranties (next 90 days) ignoring appliances without a warranty date
    warranty_data = _get_warranty_data()

    # Rooms with no circuits or outlets mapped
    unmapped_rooms = Room.objects.filter(
        Q(circuits__isnull=True) & Q(outlets__isnull=True)
    ).distinct().count()

    # Recently added
    week_ago = timezone.now() - timedelta(days=7)
    recent_count = (
        Appliance.objects.filter(created_at__gte=week_ago).count() +
        Room.objects.filter(created_at__gte=week_ago).count() +
        Circuit.objects.filter(created_at__gte=week_ago).count() +
        Outlet.objects.filter(created_at__gte=week_ago).count() +
        PaintColor.objects.filter(created_at__gte=week_ago).count()
    )

    # Appliances without a manual
    missing_docs = Appliance.objects.filter(owners_manual='').count()

    # Get recent items for activity feed
    recent_items = []
    for model_name in ['Appliance', 'Room', 'Circuit', 'Outlet', 'PaintColor']:
        try:
            model = apps.get_model('tracker', model_name)
            items = model.objects.order_by('-created_at')[:2]
            for item in items:
                recent_items.append({
                    'name': str(item),
                    'model_name': model_name,
                    'created_at': item.created_at
                })
        except LookupError:
            # Skip if model doesn't exist yet
            continue

    # Sort by creation date and limit
    recent_items = sorted(recent_items, key=lambda x: x['created_at'], reverse=True)[:10]

    context = {
        'room_count': Room.objects.count(),
        'appliance_count': Appliance.objects.count(),
        'location_count': PurchaseLocation.objects.count(),
        'paint_color_count': PaintColor.objects.count(),
        'circuit_count': Circuit.objects.count(),
        'unmapped_rooms_count': unmapped_rooms,
        'recent_items_count': recent_count,
        'missing_docs_count': missing_docs,
        'recent_items': recent_items,
        **warranty_data,
    }
    return render(request, 'tracker/home.html', context)


def missing_docs_list(request):
    """Show appliances missing documentation."""
    appliances = Appliance.objects.filter(owners_manual='').order_by('name')
    context = {
        'appliances': appliances,
        'show_create_button': False
    }
    return render(request, 'tracker/alert_cards/missing_docs_list.html', context)

def expiring_warranties_list(request):
    """Show appliances with expiring or expired warranties."""
    warranty_data = _get_warranty_data()
    warranty_data['show_create_button'] = False
    print(f"DEBUG: warranty_data = {warranty_data}")  # Add this line
    context = {
        **warranty_data,
    }
    return render(request, 'tracker/alert_cards/warranty_expiration_list.html', context)


def unmapped_rooms_list(request):
    """Show rooms with no circuits or outlets mapped."""
    rooms = Room.objects.filter(
        Q(circuits__isnull=True) & Q(outlets__isnull=True)
    ).distinct().order_by('name')

    context = {
        'rooms': rooms,
        'show_create_button': False
    }
    return render(request, 'tracker/alert_cards/unmapped_rooms_list.html', context)

def recent_additions_list(request):
    """Show recently added items."""
    recent_items = []
    for model_name in ['Appliance', 'Circuit', 'Outlet', 'PaintColor', 'Purchase_Location', 'Room']:
        try:
            model = apps.get_model('tracker', model_name)
            items = model.objects.filter(created_at__gte=timezone.now() - timedelta(days=7)).order_by('-created_at')
            for item in items:
                recent_items.append({
                    'name': str(item),
                    'model_name': model_name,
                    'created_at': item.created_at,
                    'id': item.id
                })
        except LookupError:
            continue

    # Sort by creation date
    recent_items = sorted(recent_items, key=lambda x: x['created_at'], reverse=True)

    context = {
        'recent_items': recent_items,
        'show_create_button': False,
    }
    return render(request, 'tracker/alert_cards/recent_additions_list.html', context)
