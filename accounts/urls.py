from django.urls import path
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
)
from .views import CustomUserLoginView , CustomUserLogoutView , CustomUserSignUpView ,  UserProfileUpdateView , OwnerProfileUpdateView

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomUserLoginView.as_view(), name='account_login'),
    path('logout/', CustomUserLogoutView.as_view(), name='account_logout'),
    path('signup/', CustomUserSignUpView.as_view(), name='account_signup'),
    path('profile/user_edit', UserProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/owner_update/', OwnerProfileUpdateView.as_view(), name='profile_update'),
    path('password/change/', PasswordChangeView.as_view(), name='account_change_password'),
    path('password/reset/', PasswordResetView.as_view(), name='account_reset_password'),
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='account_reset_password_confirm'),
    # Add other URLs as needed
]
