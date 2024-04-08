from typing import Tuple

from django.contrib import admin

from drug_insights_hub.research.models import ClinicalTrial, Drug, Publication


@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display: Tuple[str, str, str, str, str] = (
        "proprietary_name",
        "international_non_proprietary_name",
        "affiliated_institution",
        "drug_type",
        "development_status",
    )
    list_filter: Tuple[str, str, str] = (
        "affiliated_institution",
        "drug_type",
        "development_status",
    )
    search_fields: Tuple[str, str, str] = (
        "proprietary_name",
        "international_non_proprietary_name",
        "description",
    )


@admin.register(ClinicalTrial)
class ClinicalTrialAdmin(admin.ModelAdmin):
    list_display: Tuple[str, str, str, str, str, str] = (
        "title",
        "drug",
        "phase",
        "affiliation",
        "start_date",
        "end_date",
    )
    list_filter: Tuple[str, str] = ("phase", "affiliation")
    search_fields: Tuple[str, str, str] = ("title", "drug", "affiliation")
    date_hierarchy: str = "start_date"


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display: Tuple[str, str, str, str, str] = (
        "title",
        "publication_date",
        "modification_date",
        "affiliation",
        "journal",
    )
    list_filter: Tuple[str] = ("affiliation",)
    search_fields: Tuple[str, str] = ("title", "journal")
