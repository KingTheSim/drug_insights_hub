from django import forms
from django.contrib.auth import get_user_model

from drug_insights_hub.research.models import ClinicalTrial, Drug, Publication

USER_MODEL = get_user_model()


class DrugBaseForm(forms.ModelForm):
    class Meta:
        model = Drug
        fields = "__all__"


class DrugCreationForm(DrugBaseForm):
    pass


class DrugUpdateForm(DrugBaseForm):
    class Meta:
        model = Drug
        exclude = ("affiliated_institution",)


class DrugDeleteForm(DrugBaseForm):
    pass


class ClinicalTrialBaseForm(forms.ModelForm):
    class Meta:
        model = ClinicalTrial
        fields = "__all__"

    start_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
            },
        )
    )
    end_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
            },
        )
    )
    participants = forms.ModelMultipleChoiceField(
        queryset=USER_MODEL.objects.all(), widget=forms.SelectMultiple
    )


class ClinicalTrialCreationForm(ClinicalTrialBaseForm):
    pass


class ClinicalTrialUpdateForm(ClinicalTrialBaseForm):
    class Meta:
        model = ClinicalTrial
        exclude = (
            "drug",
            "affiliation",
        )


class ClinicalTrialDeleteForm(ClinicalTrialBaseForm):
    pass


class PublicationBaseForm(forms.ModelForm):
    class Meta:
        model = Publication
        exclude = [
            "publication_date",
            "modification_date",
        ]


class PublicationCreationForm(PublicationBaseForm):
    pass


class PublicationUpdateForm(PublicationBaseForm):
    class Meta:
        model = Publication
        exclude = [
            "publication_date",
            "modification_date",
            "affiliation",
        ]


class PublicationDeleteForm(PublicationBaseForm):
    pass
