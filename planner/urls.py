from django.urls import path
from . import views

app_name = 'planner'

urlpatterns = [
    path('', views.planner_view, name='planner_view'),
    path('get-events/', views.get_events, name='get_events'),
    path('add-event/', views.add_event, name='add_event'),
    path('edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('delete/<int:event_id>/', views.delete_event, name='delete_event'),
]
