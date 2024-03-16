from django.db import models
from django.contrib.auth import get_user_model

USER_MODEL = get_user_model()


class Affiliation(models.Model):
    MAX_NAME_LENGTH = 50
    MAX_LOCATION_LENGTH = 150

    name = models.CharField(max_length=MAX_NAME_LENGTH, unique=True)
    location = models.CharField(max_length=MAX_LOCATION_LENGTH)
    description = models.TextField()
    website = models.URLField()

    def __str__(self) -> str:
        return self.name


class UserProfile(models.Model):
    MAX_SPECIALIZATION_LENGTH = 50
    CHOICES_SPECIALIZATION = (
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

    bio = models.TextField(blank=True, null=True)
    interests = models.TextField(blank=True, null=True)
    affiliation = models.ForeignKey(Affiliation, on_delete=models.DO_NOTHING, blank=True, null=True)
    specialization = models.CharField(max_length=MAX_SPECIALIZATION_LENGTH, choices=CHOICES_SPECIALIZATION, default="Not a specialist")
    user = models.OneToOneField(USER_MODEL, on_delete=models.CASCADE, primary_key=True, name="user")

    def __str__(self) -> str:
        return self.user.get_full_name()
