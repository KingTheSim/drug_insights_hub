from django import forms
from drug_insights_hub.research.models import Drug, ClinicalTrial, Publication
from drug_insights_hub.accounts.models import Affiliation

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