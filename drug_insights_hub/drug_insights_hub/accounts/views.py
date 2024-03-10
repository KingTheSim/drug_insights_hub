from django.shortcuts import render
from django.views.generic import UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from drug_insights_hub.accounts.models import UserProfile
from drug_insights_hub.accounts.forms import UserProfileUpdateForm


class UserProfileUpdateView(UpdateView):
    model = UserProfile
    form_class = UserProfileUpdateForm
    template_name = "accounts/userprofile_update.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        return self.request.user.userprofile_set.first()
    