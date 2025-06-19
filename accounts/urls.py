from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile'),
]
