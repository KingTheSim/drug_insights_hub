from django.urls import include, path

from drug_insights_hub.research.views import drug_creation

urlpatterns = [
    path(
        "drugs/",
        include(
            [
                path("create/", drug_creation, name="drug_creation"),
            ]
        ),
    )
]
