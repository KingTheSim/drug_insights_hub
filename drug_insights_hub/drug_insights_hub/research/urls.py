from django.urls import include, path

from drug_insights_hub.research.views import (
    affiliated_clinical_trials_list,
    affiliated_drugs_list,
    affiliated_publications_list,
    clinical_trial_creation,
    clinical_trial_delete,
    clinical_trial_details,
    clinical_trial_update,
    drug_creation,
    drug_delete,
    drug_details,
    drug_update,
    publication_creation,
    publication_delete,
    publication_details,
    publication_update,
)

urlpatterns = [
    path(
        "drugs/",
        include(
            [
                path("create/", drug_creation, name="drug_creation"),
                path(
                    "affiliated_drugs_list/",
                    affiliated_drugs_list,
                    name="affiliated_drugs_list",
                ),
                path(
                    "<int:pk>/",
                    include(
                        [
                            path("update/", drug_update, name="drug_update"),
                            path("details/", drug_details, name="drug_details"),
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
                    "affiliated_clinical_trials_list/",
                    affiliated_clinical_trials_list,
                    name="affiliated_clinical_trials_list",
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
                            path(
                                "details/",
                                clinical_trial_details,
                                name="clinical_trial_details",
                            ),
                        ]
                    ),
                ),
            ]
        ),
    ),
    path(
        "publications/",
        include(
            [
                path("create/", publication_creation, name="publication_creation"),
                path(
                    "affiliated_publications_list/",
                    affiliated_publications_list,
                    name="affiliated_publications_list",
                ),
                path(
                    "<int:pk>/",
                    include(
                        [
                            path(
                                "update/", publication_update, name="publication_update"
                            ),
                            path(
                                "delete/", publication_delete, name="publication_delete"
                            ),
                            path(
                                "details/",
                                publication_details,
                                name="publication_details",
                            ),
                        ]
                    ),
                ),
            ]
        ),
    ),
]
