from django.urls import include, path

from drug_insights_hub.accounts.views import (
    UserDetailsView,
    UserLoginView,
    UserProfileUpdateView,
    UserRegistrationView,
    UserDeleteView,
)

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("delete/", UserDeleteView.as_view(), name="delete_user"),
    path(
        "profile/",
        include(
            [
                path("", UserDetailsView.as_view(), name="profile"),
                path("update/", UserProfileUpdateView.as_view(), name="profile_update"),
            ]
        ),
    ),
]
