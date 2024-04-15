from django.urls import path
from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404
from django.views import View
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
)
from .views import (
CustomUserLoginView, CustomUserLogoutView, CustomUserSignUpView,  UserProfileUpdateView,
OwnerProfileUpdateView , create_profile, edit_profile, delete_profile, accounts_management,
UserUpdateView, UserDeleteView, user_logout
)
from . import views
app_name = 'accounts'

urlpatterns = [
    path('login/', CustomUserLoginView.as_view(), name='account_login'),
    path('logout/', user_logout, name='account_logout'),
    
    path('signup/', CustomUserSignUpView.as_view(), name='account_signup'),
    path('profile/user_edit/', UserProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/owner_update/', OwnerProfileUpdateView.as_view(), name='profile_update'),
    path('password/change/', PasswordChangeView.as_view(), name='account_change_password'),
    path('password/reset/', PasswordResetView.as_view(), name='account_reset_password'),
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='account_reset_password_confirm'),
    path('user/update/<int:pk>/', UserUpdateView.as_view(), name='edit_user'),
    path('user/delete/<int:pk>/', UserDeleteView.as_view(), name='delete_user'),
    path('dashboard/', accounts_management, name='management'),
    path('profile/create/', create_profile, name='create_profile'),
    path('profile/edit/<int:pk>/', edit_profile, name='edit_profile'),
    path('profile/delete/<int:pk>/', delete_profile, name='delete_profile'),
    # Add URLs for create, edit, and delete users

]
