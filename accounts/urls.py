from django.urls import path
from django.contrib.auth.views import (
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from . import views
from .views import CustomLoginView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile'),
    path('register/', views.RegisterView.as_view(), name='register'),

    # Custom fake recovery routes
    path('password-reset/', views.fake_password_reset, name='password_reset'),
    path('password-reset/done/', views.fake_password_reset_done, name='password_reset_done'),
    path('password-reset/complete/', views.fake_password_reset_complete, name='password_reset_complete_fake'),
    path('password-reset/confirm/', views.fake_password_reset_confirm, name='password_reset_confirm_fake'),
]
