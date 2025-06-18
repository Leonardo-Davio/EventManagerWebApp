from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('events/', views.list_event, name="events"),
    path('event/<int:id>', views.event_detail, name="detail"),
    path('event/<int:id>/patecipate/', views.participation_event, name='participate'),
    path('event/<int:id>/cancel/', views.cancel_participation, name='cancel_participation'),
]
