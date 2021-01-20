from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetCompleteView
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django_email_verification import sendConfirm
import uuid # used as custom salt 
# custom form imports
from .forms import CustomUserCreationForm, UserForm, ProfileForm


class DashboardView(LoginRequiredMixin, TemplateView):
    http_method_names = ['get', 'post']
    template_name = 'django_users_app/dashboard.html'
    extra_context = {'user_form': UserForm, 'profile_form': ProfileForm}


class RegisterView(CreateView):
    http_method_names = ['get', 'post']
    template_name = 'django_users_app/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("password_reset_done")
    model = User

    def form_valid(self, form):
      user = form.save()
      returnVal = super(RegisterView, self).form_valid(form)
      sendConfirm(user, custom_salt=uuid.uuid4())
      return returnVal


class ProfileView(LoginRequiredMixin, UpdateView):
    http_method_names = ['get', 'post']
    template_name = 'profile.html'
    extra_context = {'user_form': UserForm, 'profile_form': ProfileForm}
