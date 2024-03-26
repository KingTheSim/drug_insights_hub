from django.contrib.auth.decorators import login_required
from django.core.paginator import Page, Paginator
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from drug_insights_hub.accounts.models import Affiliation
from drug_insights_hub.research.forms import (
    ClinicalTrialCreationForm,
    ClinicalTrialDeleteForm,
    ClinicalTrialUpdateForm,
    DrugCreationForm,
    DrugDeleteForm,
    DrugUpdateForm,
    PublicationCreationForm,
)
from drug_insights_hub.research.models import ClinicalTrial, Drug


@login_required
def drug_creation(request: HttpRequest) -> HttpResponse:
    form = DrugCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("index")
    else:
        return render(
            request, "research/drugs/drug_creation.html", {"form": form, "logged": True}
        )


@login_required
def drug_update(request: HttpRequest, pk: int) -> HttpResponse:
    drug = get_object_or_404(Drug, id=pk)

    user_affiliation = request.user.userprofile.affiliation

    if user_affiliation != drug.affiliated_institution:
        return HttpResponseForbidden("You do not have permission to update this drug.")

    form = DrugUpdateForm(request.POST or None, instance=drug)
    if form.is_valid():
        form.save()
        return redirect("index")
    else:
        return render(
            request,
            "research/drugs/drug_update.html",
            {"form": form, "drug": drug, "pk": pk, "logged": True},
        )


@login_required
def drug_delete(request: HttpRequest, pk: int) -> HttpResponse:
    drug = get_object_or_404(Drug, id=pk)

    user_affiliation = request.user.userprofile.affiliation

    if user_affiliation != drug.affiliated_institution:
        return HttpResponseForbidden("You do not have permission to delete this drug.")

    form = DrugDeleteForm(request.POST or None, instance=drug)
    if form.is_valid():
        drug.delete()
        return redirect("index")
    else:
        return render(
            request,
            "research/drugs/drug_delete.html",
            {"form": form, "pk": pk, "logged": True},
        )


@login_required
def affiliated_drugs_list(request: HttpRequest) -> HttpResponse:
    user_affiliation: Affiliation = request.user.userprofile.affiliation
    drugs: QuerySet[Drug] = (
        Drug.objects.filter(affiliated_institution=user_affiliation)
        .order_by("proprietary_name")
        .all()
    )
    per_page: int = 10
    paginator: Paginator = Paginator(drugs, per_page=per_page)
    page_number: int = request.GET.get("page")
    page_obj: Page = paginator.get_page(page_number)
    return render(
        request=request,
        template_name="research/drugs/affiliated_drugs_list.html",
        context={"page_obj": page_obj, "logged": True},
    )


@login_required
def clinical_trial_creation(request: HttpRequest) -> HttpResponse:
    form = ClinicalTrialCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("index")
    else:
        return render(
            request,
            "research/clinical_trials/clinical_trial_creation.html",
            {"form": form, "logged": True},
        )


@login_required
def clinical_trial_update(request: HttpRequest, pk: int) -> HttpResponse:
    clinical_trial = get_object_or_404(ClinicalTrial, pk=pk)
    user_affiliation = request.user.userprofile.affiliation

    if user_affiliation != clinical_trial.affiliation:
        return HttpResponseForbidden(
            "You do not have permission to update this clinical trial."
        )

    form = ClinicalTrialUpdateForm(request.POST or None, instance=clinical_trial)
    if form.is_valid():
        form.save()
        return redirect("index")
    else:
        return render(
            request,
            "research/clinical_trials/clinical_trial_update.html",
            {"form": form, "pk": pk, "logged": True},
        )


@login_required
def clinical_trial_delete(request: HttpRequest, pk: int) -> HttpResponse:
    clinical_trial = get_object_or_404(ClinicalTrial, pk=pk)
    user_affiliation = request.user.userprofile.affiliation

    if user_affiliation != clinical_trial.affiliation:
        return HttpResponseForbidden(
            "You do not have permission to delete this clinical trial."
        )

    form = ClinicalTrialDeleteForm(request.POST or None, instance=clinical_trial)
    if form.is_valid():
        clinical_trial.delete()
        return redirect("index")
    else:
        return render(
            request,
            "research/clinical_trials/clinical_trial_delete.html",
            {"form": form, "pk": pk, "logged": True},
        )


@login_required
def affiliated_clinical_trials_list(request: HttpRequest) -> HttpResponse:
    user_affiliation: Affiliation = request.user.userprofile.affiliation
    clinical_trials: QuerySet[ClinicalTrial] = (
        ClinicalTrial.objects.filter(affiliation=user_affiliation)
        .order_by("title")
        .all()
    )
    per_page: int = 10
    paginator: Paginator = Paginator(clinical_trials, per_page=per_page)
    page_number: int = request.GET.get("page")
    page_obj: Page = paginator.get_page(page_number)
    return render(
        request=request,
        template_name="research/clinical_trials/affiliated_clinical_trials_list.html",
        context={"page_obj": page_obj, "logged": True},
    )


@login_required
def publication_creation(request: HttpRequest) -> HttpResponse:
    form: PublicationCreationForm = PublicationCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("index")
    else:
        return render(
            request=request,
            template_name="research/publications/publication_creation.html",
            context={"form": form, "logged": True},
        )
