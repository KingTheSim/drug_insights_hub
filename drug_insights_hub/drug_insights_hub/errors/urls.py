from django.urls import path
from drug_insights_hub.errors.views import error

urlpatterns = [
    path("", error, name="error"),
]
