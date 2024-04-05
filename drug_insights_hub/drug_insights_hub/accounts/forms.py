from typing import Tuple, Type

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User

from drug_insights_hub.accounts.models import UserProfile

USER_MODEL: Type[User] = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].widget.attrs.update({"class": "form-control"})

    class Meta(UserCreationForm.Meta):
        model: User = USER_MODEL
        fields: Tuple[str, str, str] = ("username", "first_name", "last_name")


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model: User = USER_MODEL
        fields: Tuple[str, str, str] = ("username", "first_name", "last_name")


class UserProfileBaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].widget.attrs.update({"class": "form-control"})

    class Meta:
        model: User = UserProfile
        exclude: Tuple[str, str] = ("affiliation", "user")


class UserProfileUpdateForm(UserProfileBaseForm):
    pass
