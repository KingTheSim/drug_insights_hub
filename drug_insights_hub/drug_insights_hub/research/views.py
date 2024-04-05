from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
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
    PublicationDeleteForm,
    PublicationUpdateForm,
)
from drug_insights_hub.research.models import ClinicalTrial, Drug, Publication


@login_required
def drug_creation(request: HttpRequest) -> HttpResponse:
    form: DrugCreationForm = DrugCreationForm(request.POST or None, user=request.user)
    affiliation_variable: Affiliation = affiliation_getter(request=request)
    if form.is_valid():
        drug: Drug = form.save(commit=False)
        drug.affiliated_institution = affiliation_variable
        form.save()
        return redirect("affiliated_drugs_list")
    else:
        return render(
            request=request,
            template_name="research/drugs/drug_creation.html",
            context={
                "form": form,
                "logged": True,
            },
        )


@login_required
def drug_update(request: HttpRequest, pk: int) -> HttpResponse:
    drug: Drug = get_object_or_404(Drug, id=pk)

    user_affiliation: Affiliation = affiliation_getter(request=request)

    if user_affiliation != drug.affiliated_institution:
        return HttpResponseForbidden("You do not have permission to update this drug.")

    form: DrugUpdateForm = DrugUpdateForm(request.POST or None, instance=drug)
    if form.is_valid():
        form.save()
        return redirect("affiliated_drugs_list")
    else:
        return render(
            request=request,
            template_name="research/drugs/drug_update.html",
            context={"form": form, "drug": drug, "pk": pk, "logged": True},
        )


@login_required
def drug_delete(request: HttpRequest, pk: int) -> HttpResponse:
    drug: Drug = get_object_or_404(Drug, id=pk)

    user_affiliation: Affiliation = affiliation_getter(request=request)

    if user_affiliation != drug.affiliated_institution:
        return HttpResponseForbidden("You do not have permission to delete this drug.")

    form: DrugDeleteForm = DrugDeleteForm(request.POST or None, instance=drug)
    if form.is_valid():
        drug.delete()
        return redirect("affiliated_drugs_list")
    else:
        return render(
            request=request,
            template_name="research/drugs/drug_delete.html",
            context={"form": form, "pk": pk, "logged": True},
        )


@login_required
def affiliated_drugs_list(request: HttpRequest) -> HttpResponse:
    user_affiliation: Affiliation = affiliation_getter(request=request)
    drugs: QuerySet[Drug] = (
        Drug.objects.filter(affiliated_institution=user_affiliation)
        .order_by("proprietary_name")
        .all()
    )
    per_page: int = 9
    paginator: Paginator = Paginator(drugs, per_page=per_page)
    page_number: int = request.GET.get("page")
    page_obj: Page = paginator.get_page(page_number)
    return render(
        request=request,
        template_name="research/drugs/affiliated_drugs_list.html",
        context={"page_obj": page_obj, "logged": True},
    )


def drug_details(request: HttpRequest, pk: int) -> HttpResponse:
    drug: Drug = get_object_or_404(Drug, pk=pk)
    has_rights: bool = False
    logged: bool = False
    if request.user.is_authenticated:
        logged = True
        user_affiliation: Affiliation = request.user.userprofile.affiliation
        if user_affiliation == drug.affiliated_institution:
            has_rights = True

    return render(
        request=request,
        template_name="research/drugs/drug_details.html",
        context={"drug": drug, "has_rights": has_rights, "logged": logged},
    )


@login_required
def clinical_trial_creation(request: HttpRequest) -> HttpResponse:
    form: ClinicalTrialCreationForm = ClinicalTrialCreationForm(
        request.POST or None, user=request.user
    )
    affiliation_variable: Affiliation = affiliation_getter(request=request)
    if form.is_valid():
        clinical_trial: ClinicalTrial = form.save(commit=False)
        clinical_trial.affiliation = affiliation_variable
        form.save()
        return redirect("affiliated_clinical_trials_list")
    else:
        return render(
            request=request,
            template_name="research/clinical_trials/clinical_trial_creation.html",
            context={"form": form, "logged": True},
        )


@login_required
def clinical_trial_update(request: HttpRequest, pk: int) -> HttpResponse:
    clinical_trial: ClinicalTrial = get_object_or_404(ClinicalTrial, pk=pk)
    user_affiliation: Affiliation = affiliation_getter(request=request)

    if user_affiliation != clinical_trial.affiliation:
        return HttpResponseForbidden(
            "You do not have permission to update this clinical trial."
        )

    form: ClinicalTrialUpdateForm = ClinicalTrialUpdateForm(
        request.POST or None, instance=clinical_trial
    )
    if form.is_valid():
        form.save()
        return redirect("affiliated_clinical_trials_list")
    else:
        return render(
            request=request,
            template_name="research/clinical_trials/clinical_trial_update.html",
            context={"form": form, "pk": pk, "logged": True},
        )


@login_required
def clinical_trial_delete(request: HttpRequest, pk: int) -> HttpResponse:
    clinical_trial: ClinicalTrial = get_object_or_404(ClinicalTrial, pk=pk)
    user_affiliation: Affiliation = affiliation_getter(request=request)

    if user_affiliation != clinical_trial.affiliation:
        return HttpResponseForbidden(
            "You do not have permission to delete this clinical trial."
        )

    form: ClinicalTrialDeleteForm = ClinicalTrialDeleteForm(
        request.POST or None, instance=clinical_trial
    )
    if form.is_valid():
        clinical_trial.delete()
        return redirect("affiliated_clinical_trials_list")
    else:
        return render(
            request=request,
            template_name="research/clinical_trials/clinical_trial_delete.html",
            context={"form": form, "pk": pk, "logged": True},
        )


@login_required
def affiliated_clinical_trials_list(request: HttpRequest) -> HttpResponse:
    user_affiliation: Affiliation = affiliation_getter(request=request)
    clinical_trials: QuerySet[ClinicalTrial] = (
        ClinicalTrial.objects.filter(affiliation=user_affiliation)
        .order_by("title")
        .all()
    )
    per_page: int = 9
    paginator: Paginator = Paginator(clinical_trials, per_page=per_page)
    page_number: int = request.GET.get("page")
    page_obj: Page = paginator.get_page(page_number)
    return render(
        request=request,
        template_name="research/clinical_trials/affiliated_clinical_trials_list.html",
        context={"page_obj": page_obj, "logged": True},
    )


def clinical_trial_details(request: HttpRequest, pk: int) -> HttpResponse:
    clinical_trial: ClinicalTrial = get_object_or_404(ClinicalTrial, pk=pk)
    has_rights: bool = False
    logged: bool = False
    if request.user.is_authenticated:
        logged = True
        user_affiliation: Affiliation = request.user.userprofile.affiliation
        if user_affiliation == clinical_trial.affiliation:
            has_rights = True

    return render(
        request=request,
        template_name="research/clinical_trials/clinical_trial_details.html",
        context={
            "clinical_trial": clinical_trial,
            "logged": logged,
            "has_rights": has_rights,
        },
    )


@login_required
def publication_creation(request: HttpRequest) -> HttpResponse:
    form: PublicationCreationForm = PublicationCreationForm(
        request.POST or None, user=request.user
    )
    affiliation_variable: Affiliation = affiliation_getter(request=request)
    if form.is_valid():
        publication: Publication = form.save(commit=False)
        publication.affiliation = affiliation_variable
        form.save()
        return redirect("affiliated_publications_list")
    else:
        return render(
            request=request,
            template_name="research/publications/publication_creation.html",
            context={"form": form, "logged": True},
        )


@login_required
def publication_update(request: HttpRequest, pk: int) -> HttpResponse:
    publication: Publication = get_object_or_404(Publication, pk=pk)
    user_affiliation: Affiliation = affiliation_getter(request=request)

    if user_affiliation != publication.affiliation:
        return HttpResponseForbidden(
            "You do not have permission to update this publication."
        )

    form: PublicationUpdateForm = PublicationUpdateForm(
        request.POST or None, instance=publication
    )
    if form.is_valid():
        form.save()
        return redirect("affiliated_publications_list")
    else:
        return render(
            request=request,
            template_name="research/publications/publication_update.html",
            context={"form": form, "pk": pk, "logged": True},
        )


@login_required
def publication_delete(request: HttpRequest, pk: int) -> HttpResponse:
    publication: Publication = get_object_or_404(Publication, pk=pk)
    user_affiliation: Affiliation = affiliation_getter(request=request)

    if user_affiliation != publication.affiliation:
        return HttpResponseForbidden(
            "You do not have permission to delete this publication."
        )

    form: PublicationDeleteForm = PublicationDeleteForm(
        request.POST or None, instance=publication
    )
    if form.is_valid():
        publication.delete()
        return redirect("affiliated_publications_list")
    else:
        return render(
            request=request,
            template_name="research/publications/publication_delete.html",
            context={"form": form, "pk": pk, "logged": True},
        )


@login_required
def affiliated_publications_list(request: HttpRequest) -> HttpResponse:
    user_affiliation: Affiliation = affiliation_getter(request=request)
    publications: QuerySet[Publication] = (
        Publication.objects.filter(affiliation=user_affiliation).order_by("title").all()
    )
    per_page: int = 9
    paginator: Paginator = Paginator(publications, per_page=per_page)
    page_number: int = request.GET.get("page")
    page_obj: Page = paginator.get_page(page_number)
    return render(
        request=request,
        template_name="research/publications/affiliated_publications_list.html",
        context={"page_obj": page_obj, "logged": True},
    )


@login_required
def publication_details(request: HttpRequest, pk: int) -> HttpResponse:
    publication: Publication = get_object_or_404(Publication, pk=pk)
    has_rights: bool = False
    logged: bool = False
    affiliation_variable: Affiliation = affiliation_getter(request=request)
    if request.user.is_authenticated:
        logged = True
        user_affiliation: Affiliation = affiliation_variable
        if user_affiliation == publication.affiliation:
            has_rights = True

    return render(
        request=request,
        template_name="research/publications/publication_details.html",
        context={
            "publication": publication,
            "logged": logged,
            "has_rights": has_rights,
        },
    )


def affiliation_getter(request: HttpRequest) -> HttpResponse | Affiliation:
    affiliation_result: Affiliation = request.user.userprofile.affiliation
    if affiliation_result is None:
        raise PermissionDenied("You do not have an affiliation!")
    else:
        return affiliation_result
