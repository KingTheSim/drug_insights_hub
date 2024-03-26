from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from drug_insights_hub.accounts.forms import (
    CustomUserCreationForm,
    UserProfileUpdateForm,
)

USER_MODEL = get_user_model()


class UserProfileUpdateView(UpdateView, LoginRequiredMixin):
    form_class = UserProfileUpdateForm
    template_name = "accounts/userprofile_update.html"
    success_url = reverse_lazy("profile")
    custom_context = {"logged": True}

    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context.update(self.custom_context)
        return context

    def get_object(self, queryset=None):
        return self.request.user.userprofile


class UserRegistrationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("index")
    custom_context = {"logged": False}

    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context.update(self.custom_context)
        return context


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    success_url = reverse_lazy("index")
    custom_context = {"logged": False}

    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context.update(self.custom_context)
        return context


class UserDeleteView(DeleteView, LoginRequiredMixin):
    model = USER_MODEL
    template_name = "accounts/delete.html"
    success_url = reverse_lazy("index")
    custom_context = {"logged": True}

    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context.update(self.custom_context)
        return context


class UserDetailsView(DetailView, LoginRequiredMixin):
    model = USER_MODEL
    template_name = "accounts/profile.html"
    context_object_name = "user"
    custom_context = {"logged": True}

    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context.update(self.custom_context)
        return context

    def get_object(self, queryset=None):
        return self.request.user
