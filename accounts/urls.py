from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import (
    CustomLoginView,
    FakePasswordResetView,
    FakePasswordResetDoneView,
    FakePasswordResetConfirmView,
    FakePasswordResetCompleteView,
)

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile'),
    path('register/', views.RegisterView.as_view(), name='register'),

    # Custom fake recovery routes
    path('password-reset/', FakePasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', FakePasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/complete/', FakePasswordResetCompleteView.as_view(), name='password_reset_complete_fake'),
    path('password-reset/confirm/', FakePasswordResetConfirmView.as_view(), name='password_reset_confirm_fake'),
]
