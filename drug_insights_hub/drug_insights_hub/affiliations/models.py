from django.db import models

class Affiliation(models.Model):
    MAX_NAME_LENGTH = 50
    MAX_LOCATION_LENGTH = 150

    name = models.CharField(max_length=MAX_NAME_LENGTH, unique=True)
    location = models.CharField(max_length=MAX_LOCATION_LENGTH)
    description = models.TextField()
    website = models.URLField()

    def __str__(self) -> str:
        return self.name