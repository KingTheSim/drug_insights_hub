from django.urls import include, path

from drug_insights_hub.research.views import (
    affiliated_drugs_list,
    clinical_trial_creation,
    clinical_trial_delete,
    clinical_trial_update,
    drug_creation,
    drug_delete,
    drug_update,
    publication_creation,
)

urlpatterns = [
    path(
        "drugs/",
        include(
            [
                path("create/", drug_creation, name="drug_creation"),
                path("affiliated_drugs_list/", affiliated_drugs_list, name="affiliated_drugs_list"),
                path(
                    "<int:pk>/",
                    include(
                        [
                            path("update/", drug_update, name="drug_update"),
                            path("delete/", drug_delete, name="drug_delete"),
                        ]
                    ),
                ),
            ]
        ),
    ),
    path(
        "clinical_trials/",
        include(
            [
                path(
                    "create/", clinical_trial_creation, name="clinical_trial_creation"
                ),
                path(
                    "<int:pk>/",
                    include(
                        [
                            path(
                                "update/",
                                clinical_trial_update,
                                name="clinical_trial_update",
                            ),
                            path(
                                "delete/",
                                clinical_trial_delete,
                                name="clinical_trial_delete",
                            ),
                        ]
                    ),
                ),
            ]
        ),
    ),
    path("publications/", include([
        path("create/", publication_creation, name="publication_creation"),
    ]))
]
