# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .forms import CustomUserCreationForm, UserProfileForm, OwnerProfileForm
from .models import CustomUser, UserProfile, OwnerProfile

class CustomUserLoginView(LoginView):
    template_name = 'accounts/login.html'

class CustomUserLogoutView(LogoutView):
    template_name = 'accounts/logout.html'
    next_page = reverse_lazy('home')

class CustomUserSignUpView(UpdateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

    def get_success_url(self):
        return reverse_lazy('home')

@login_required
def profile(request):
    user_profile = UserProfile.objects.get_or_create(user=request.user)[0]
    owner_profile = OwnerProfile.objects.get_or_create(user=request.user)[0]

    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        owner_form = OwnerProfileForm(request.POST, request.FILES, instance=owner_profile)

        if user_form.is_valid() and owner_form.is_valid():
            user_form.save()
            owner_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')

    else:
        user_form = UserProfileForm(instance=user_profile)
        owner_form = OwnerProfileForm(instance=owner_profile)

    return render(request, 'accounts/profile.html', {'user_form': user_form, 'owner_form': owner_form})
