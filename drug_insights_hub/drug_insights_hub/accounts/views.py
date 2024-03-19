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

    def get_object(self, queryset=None):
        return self.request.user.userprofile


class UserRegistrationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("index")


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    success_url = reverse_lazy("index")


class UserDeleteView(DeleteView, LoginRequiredMixin):
    model = USER_MODEL
    template_name = "accounts/delete.html"
    success_url = reverse_lazy("index")


class UserDetailsView(DetailView, LoginRequiredMixin):
    model = USER_MODEL
    template_name = "accounts/profile.html"
    context_object_name = "user"

    def get_object(self, queryset=None):
        return self.request.user
