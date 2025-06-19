from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('events/', views.list_event, name="events"),
    path('event/<int:id>', views.event_detail, name="detail"),
    path('event/<int:id>/participate/', views.participation_event, name='participate'),
    path('event/<int:id>/cancel/', views.cancel_participation, name='cancel_participation'),
    path('new_event/', views.new_event, name="new_event"),
    path('event/<int:id>/edit/', views.manage_event, name="edit_event"),
]