from typing import Tuple

from django.contrib import admin

from drug_insights_hub.accounts.models import Affiliation, UserProfile


@admin.register(Affiliation)
class AffiliationAdmin(admin.ModelAdmin):
    list_display: Tuple[str, str, str, str] = (
        "name",
        "location",
        "description",
        "website",
    )
    list_filter: Tuple[str, str, str, str] = (
        "name",
        "location",
        "description",
        "website",
    )
    search_fields: Tuple[str, str, str, str] = (
        "name",
        "location",
        "description",
        "website",
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display: Tuple[str, str, str, str] = (
        "bio",
        "interests",
        "specialization",
        "user",
    )
    list_filter: Tuple[str, str, str, str] = (
        "bio",
        "interests",
        "specialization",
        "user",
    )
    search_fields: Tuple[str, str, str, str] = (
        "bio",
        "interests",
        "specialization",
        "user",
    )
