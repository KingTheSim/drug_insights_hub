from typing import Type

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from drug_insights_hub.accounts.models import Affiliation

USER_MODEL: Type[User] = get_user_model()


class Drug(models.Model):
    MAX_PROPRIETARY_NAME_LENGTH: int = 50

    MAX_INTERNATIONAL_NON_PROPRIETARY_NAME_LENGTH: int = 50

    MAX_TYPE_LENGTH: int = 30
    CHOICES_TYPES: tuple = (
        ("Therapeutic", "Therapeutic"),
        ("Experimental", "Experimental"),
        ("Preventive", "Preventive"),
        ("Diagnostic", "Diagnostic"),
        ("Palliative", "Palliative"),
        ("Combination", "Combination"),
        ("Over-the-Counter (OTC)", "Over-the-Counter (OTC)"),
        ("Generic", "Generic"),
        ("Biological", "Biological"),
        ("Orphan", "Orphan"),
        ("Herbal/Alternative", "Herbal/Alternative"),
        ("Radiopharmaceutical", "Radiopharmaceutical"),
    )

    MAX_DEVELOPMENT_STATUS_LENGTH: int = 30
    CHOICES_DEVELOPMENT_STATUS: tuple = (
        ("Preclinical", "Preclinical"),
        ("Phase I", "Phase I"),
        ("Phase II", "Phase II"),
        ("Phase III", "Phase III"),
        ("Approved", "Approved"),
    )

    proprietary_name: models.CharField = models.CharField(
        max_length=MAX_PROPRIETARY_NAME_LENGTH, unique=True, blank=True, null=True
    )
    international_non_proprietary_name: models.CharField = models.CharField(
        max_length=MAX_INTERNATIONAL_NON_PROPRIETARY_NAME_LENGTH
    )
    affiliated_institution: Type[Affiliation] = models.ForeignKey(
        Affiliation, on_delete=models.DO_NOTHING
    )
    drug_type: models.CharField = models.CharField(
        max_length=MAX_TYPE_LENGTH, choices=CHOICES_TYPES, blank=True, null=True
    )
    development_status: models.CharField = models.CharField(
        max_length=MAX_DEVELOPMENT_STATUS_LENGTH,
        choices=CHOICES_DEVELOPMENT_STATUS,
        default="Preclinical",
    )
    description: models.TextField = models.TextField()

    def __str__(self) -> str:
        return self.proprietary_name


class ClinicalTrial(models.Model):
    MAX_TITLE_LENGTH: int = 50

    MAX_PHASE_LENGTH: int = 30
    CHOICES_PHASE_STATUS: tuple = (
        ("Preclinical", "Preclinical"),
        ("Phase I", "Phase I"),
        ("Phase II", "Phase II"),
        ("Phase III", "Phase III"),
        ("Approved", "Approved"),
    )

    title: models.CharField = models.CharField(max_length=MAX_TITLE_LENGTH, unique=True)
    drug: Type[Drug] = models.ForeignKey(Drug, on_delete=models.DO_NOTHING)
    phase: models.CharField = models.CharField(
        max_length=MAX_PHASE_LENGTH, choices=CHOICES_PHASE_STATUS
    )
    participants: Type[User] = models.ManyToManyField(USER_MODEL)
    affiliation: Type[Affiliation] = models.ForeignKey(
        Affiliation, on_delete=models.DO_NOTHING
    )
    start_date: models.DateField = models.DateField()
    end_date: models.DateField = models.DateField()
    description: models.TextField = models.TextField()

    def clean(self) -> None:
        super().clean()

        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("Start date must be before or equal to end date.")

    def save(self, *args, **kwargs) -> None:
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class Publication(models.Model):
    MAX_TITLE_LENGTH: int = 50

    MAX_JOURNAL_LENGTH: int = 30

    title: models.CharField = models.CharField(max_length=MAX_TITLE_LENGTH, unique=True)
    authors: Type[User] = models.ManyToManyField(USER_MODEL)
    trials: Type[ClinicalTrial] = models.ManyToManyField(ClinicalTrial)
    affiliation: Type[Affiliation] = models.ForeignKey(
        Affiliation, on_delete=models.DO_NOTHING
    )
    publication_date: models.DateField = models.DateField(auto_now_add=True)
    modification_date: models.DateField = models.DateField(auto_now=True)
    journal: models.CharField = models.CharField(max_length=MAX_JOURNAL_LENGTH)

    def __str__(self) -> str:
        return self.title
