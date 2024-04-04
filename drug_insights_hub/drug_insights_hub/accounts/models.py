from typing import Optional, Tuple, Type

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models

USER_MODEL: Type[User] = get_user_model()


class Affiliation(models.Model):
    MAX_NAME_LENGTH: int = 50
    MAX_LOCATION_LENGTH: int = 150

    name: models.CharField = models.CharField(max_length=MAX_NAME_LENGTH, unique=True)
    location: models.CharField = models.CharField(max_length=MAX_LOCATION_LENGTH)
    description: models.TextField = models.TextField()
    website: models.URLField = models.URLField()

    def __str__(self) -> str:
        return self.name


class UserProfile(models.Model):
    MAX_SPECIALIZATION_LENGTH: int = 50
    CHOICES_SPECIALIZATION: Tuple[Tuple[str, str], ...] = (
        ("Not a specialist", "Not a specialist"),
        ("Pharmaceutical Researcher", "Pharmaceutical Researcher"),
        ("Clinical Trial Investigator", "Clinical Trial Investigator"),
        ("Drug Development Scientist", "Drug Development Scientist"),
        ("Regulatory Affairs Specialist", "Regulatory Affairs Specialist"),
        ("Medical Writer", "Medical Writer"),
        ("Healthcare Professional", "Healthcare Professional"),
        ("Pharmacologist", "Pharmacologist"),
        ("Biostatistician", "Biostatistician"),
    )

    bio: Optional[models.TextField] = models.TextField(blank=True, null=True)
    interests: Optional[models.TextField] = models.TextField(blank=True, null=True)
    affiliation: Optional[Affiliation] = models.ForeignKey(
        Affiliation, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    specialization: models.CharField = models.CharField(
        max_length=MAX_SPECIALIZATION_LENGTH,
        choices=CHOICES_SPECIALIZATION,
        default="Not a specialist",
    )
    user: User = models.OneToOneField(
        USER_MODEL, on_delete=models.CASCADE, primary_key=True
    )

    def __str__(self) -> str:
        return self.user.get_full_name()
