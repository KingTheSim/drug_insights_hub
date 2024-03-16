from django.urls import path
from drug_insights_hub.core.views import index

urlpatterns = [
    path('', index, name="index"),
]