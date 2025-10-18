from django.urls import path
from vehicles import views

app_name = 'vehicles'

urlpatterns = [
    path('', views.list, name='list'),
    path('create/', views.create, name='create'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/edit/', views.update, name='update'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('<int:vehicle_id>/maintenance/add/', views.add_maintenance, name='add_maintenance'),
]
