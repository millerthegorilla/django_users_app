from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy

# activated form imports
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView

from django_email_verification import sendConfirm

# custom form imports
from .forms import CustomUserCreationForm, UserForm, ProfileForm
import uuid
# customized token generation
from .tokens import AccountActivationTokenGenerator
from django.views.decorators.csrf import csrf_protect
# Create your views here.


class UserLoginView(LoginView):
    redirect_authenticated_user = True
    success_url = 'users/dashboard.html'

    # def dispatch(self, request, *args, **kwargs):
    #     print("HELLO")
    #     return super().dispatch(request, *args, **kwargs)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'users/dashboard.html'
    extra_context = {'user_form': UserForm, 'profile_form': ProfileForm}


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:login")
    model = User
    
    def form_valid(self, form):
      user = form.save()
      returnVal = super(RegisterView, self).form_valid(form)
      sendConfirm(user, custom_salt=uuid.uuid4())
      return returnVal

class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'users/profile.html'
    extra_context = {'user_form': UserForm, 'profile_form': ProfileForm}