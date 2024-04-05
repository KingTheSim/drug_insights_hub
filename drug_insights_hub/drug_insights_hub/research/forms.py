from typing import Tuple, Type

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from drug_insights_hub.research.models import ClinicalTrial, Drug, Publication

USER_MODEL: Type[User] = get_user_model()


class DrugBaseForm(forms.ModelForm):
    class Meta:
        model: Type[Drug] = Drug
        fields: str = "__all__"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].widget.attrs.update({"class": "form-control"})


class DrugCreationForm(DrugBaseForm):
    def __init__(self, *args, **kwargs) -> None:
        user: Type[User] = kwargs.pop("user", None)
        super(DrugCreationForm, self).__init__(*args, **kwargs)
        if user and user.userprofile.affiliation:
            self.fields["affiliated_institution"].initial = user.userprofile.affiliation
            self.fields["affiliated_institution"].widget.attrs["readonly"] = True
            self.fields["affiliated_institution"].widget.attrs["disabled"] = True
            self.fields["affiliated_institution"].required = False

        for field in self.fields.keys():
            self.fields[field].widget.attrs.update({"class": "form-control"})


class DrugUpdateForm(DrugBaseForm):
    class Meta:
        model: Type[Drug] = Drug
        exclude: Tuple[str,] = ("affiliated_institution",)


class DrugDeleteForm(DrugBaseForm):
    pass


class ClinicalTrialBaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].widget.attrs.update({"class": "form-control"})

    class Meta:
        model: Type[ClinicalTrial] = ClinicalTrial
        fields: str = "__all__"

    start_date: forms.DateField = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
            },
        )
    )
    end_date: forms.DateField = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
            },
        )
    )
    participants: forms.MultipleChoiceField = forms.ModelMultipleChoiceField(
        queryset=USER_MODEL.objects.all(), widget=forms.SelectMultiple
    )


class ClinicalTrialCreationForm(ClinicalTrialBaseForm):
    def __init__(self, *args, **kwargs) -> None:
        user: Type[User] = kwargs.pop("user", None)
        super(ClinicalTrialCreationForm, self).__init__(*args, **kwargs)
        if user and user.userprofile.affiliation:
            self.fields["affiliation"].initial = user.userprofile.affiliation
            self.fields["affiliation"].widget.attrs["readonly"] = True
            self.fields["affiliation"].widget.attrs["disabled"] = True
            self.fields["affiliation"].required = False

        for field in self.fields.keys():
            self.fields[field].widget.attrs.update({"class": "form-control"})


class ClinicalTrialUpdateForm(ClinicalTrialBaseForm):
    class Meta:
        model: Type[ClinicalTrial] = ClinicalTrial
        exclude: Tuple[str, str] = (
            "drug",
            "affiliation",
        )


class ClinicalTrialDeleteForm(ClinicalTrialBaseForm):
    pass


class PublicationBaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].widget.attrs.update({"class": "form-control"})

    class Meta:
        model: Type[Publication] = Publication
        exclude: Tuple[str, str] = (
            "publication_date",
            "modification_date",
        )


class PublicationCreationForm(PublicationBaseForm):
    def __init__(self, *args, **kwargs):
        user: Type[User] = kwargs.pop("user", None)
        super(PublicationCreationForm, self).__init__(*args, **kwargs)
        if user and user.userprofile.affiliation:
            self.fields["affiliation"].initial = user.userprofile.affiliation
            self.fields["affiliation"].widget.attrs["readonly"] = True
            self.fields["affiliation"].widget.attrs["disabled"] = True
            self.fields["affiliation"].required = False

        for field in self.fields.keys():
            self.fields[field].widget.attrs.update({"class": "form-control"})


class PublicationUpdateForm(PublicationBaseForm):
    class Meta:
        model: Type[Publication] = Publication
        exclude: Tuple[str, str, str] = (
            "publication_date",
            "modification_date",
            "affiliation",
        )


class PublicationDeleteForm(PublicationBaseForm):
    pass
