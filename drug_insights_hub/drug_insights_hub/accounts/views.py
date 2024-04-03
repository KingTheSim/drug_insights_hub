from typing import Dict, Type

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from drug_insights_hub.accounts.forms import (
    CustomUserCreationForm,
    UserProfileUpdateForm,
)
from drug_insights_hub.accounts.models import UserProfile

USER_MODEL: Type[User] = get_user_model()


class UserProfileUpdateView(UpdateView, LoginRequiredMixin):
    form_class: Type[UserProfileUpdateForm] = UserProfileUpdateForm
    template_name: str = "accounts/userprofile_update.html"
    success_url: str = reverse_lazy("profile")
    custom_context: Dict[str, bool] = {"logged": True}

    def get_context_data(self, **kwargs) -> Dict[str, any]:
        context: Dict[str, bool] = super().get_context_data(**kwargs)
        context.update(self.custom_context)
        return context

    def get_object(self, queryset=None) -> UserProfile:
        return self.request.user.userprofile


class UserRegistrationView(CreateView):
    form_class: Type[CustomUserCreationForm] = CustomUserCreationForm
    template_name: str = "accounts/register.html"
    success_url: str = reverse_lazy("index")
    custom_context: Dict[str, bool] = {"logged": False}

    def get_context_data(self, **kwargs) -> Dict[str, any]:
        context: Dict[str, bool] = super().get_context_data(**kwargs)
        context.update(self.custom_context)
        return context


class UserLoginView(LoginView):
    template_name: str = "accounts/login.html"
    success_url: str = reverse_lazy("index")
    custom_context: Dict[str, bool] = {"logged": False}

    def get_context_data(self, **kwargs) -> Dict[str, any]:
        context: Dict[str, bool] = super().get_context_data(**kwargs)
        context.update(self.custom_context)
        return context


class UserDeleteView(DeleteView, LoginRequiredMixin):
    model: Type[User] = USER_MODEL
    template_name: str = "accounts/delete.html"
    success_url: str = reverse_lazy("index")
    custom_context: Dict[str, bool] = {"logged": True}

    def get_context_data(self, **kwargs) -> Dict[str, any]:
        context: Dict[str, bool] = super().get_context_data(**kwargs)
        context.update(self.custom_context)
        return context


class UserDetailsView(DetailView, LoginRequiredMixin):
    model: Type[User] = USER_MODEL
    template_name: str = "accounts/profile.html"
    context_object_name: str = "user"
    custom_context: Dict[str, bool] = {"logged": True}

    def get_context_data(self, **kwargs) -> Dict[str, any]:
        context: Dict[str, bool] = super().get_context_data(**kwargs)
        context.update(self.custom_context)
        return context

    def get_object(self, queryset=None) -> User:
        return self.request.user
