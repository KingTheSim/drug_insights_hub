from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from drug_insights_hub.accounts.models import UserProfile

USER_MODEL = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = USER_MODEL
        fields = ("username", "first_name", "last_name")


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = USER_MODEL
        fields = ("username", "first_name", "last_name")


class UserProfileBaseForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ("affiliation", "user")


class UserProfileUpdateForm(UserProfileBaseForm):
    pass
