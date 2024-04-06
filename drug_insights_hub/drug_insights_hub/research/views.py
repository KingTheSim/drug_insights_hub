from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Page, Paginator
from django.db.models import QuerySet
from django.http import Http404, HttpRequest, HttpResponse
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
    try:
        affiliation_variable: Affiliation = affiliation_getter(request=request)
    except PermissionDenied as e:
        request.session["error_message"] = str(e)
        request.session["status_code"] = 403
        return redirect("error")

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
    try:
        drug: Drug = get_object_or_404(Drug, id=pk)
    except Http404:
        request.session["error_message"] = "Drug not found!"
        request.session["status_code"] = 404
        return redirect("error")

    try:
        user_affiliation: Affiliation = affiliation_getter(request=request)
    except PermissionDenied as e:
        request.session["error_message"] = str(e)
        request.session["status_code"] = 403
        return redirect("error")

    if user_affiliation != drug.affiliated_institution:
        request.session["error_message"] = (
            "Your affiliation doesn't match the drug's affiliation, so you lack permission!"
        )
        request.session["status_code"] = 403
        return redirect("error")

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
    try:
        drug: Drug = get_object_or_404(Drug, id=pk)
    except Http404:
        request.session["error_message"] = "Drug not found!"
        request.session["status_code"] = 404
        return redirect("error")

    try:
        user_affiliation: Affiliation = affiliation_getter(request=request)
    except PermissionDenied as e:
        request.session["error_message"] = str(e)
        request.session["status_code"] = 403
        return redirect("error")

    if user_affiliation != drug.affiliated_institution:
        request.session["error_message"] = (
            "Your affiliation doesn't match the drug's affiliation, so you lack permission!"
        )
        request.session["status_code"] = 403
        return redirect("error")

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
    try:
        user_affiliation: Affiliation = affiliation_getter(request=request)
    except PermissionDenied as e:
        request.session["error_message"] = str(e)
        request.session["status_code"] = 403
        return redirect("error")

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
    try:
        drug: Drug = get_object_or_404(Drug, pk=pk)
    except Http404:
        request.session["error_message"] = "Drug not found!"
        request.session["status_code"] = 404
        return redirect("error")

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
    try:
        affiliation_variable: Affiliation = affiliation_getter(request=request)
    except PermissionDenied as e:
        request.session["error_message"] = str(e)
        request.session["status_code"] = 403
        return redirect("error")

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
    try:
        clinical_trial: ClinicalTrial = get_object_or_404(ClinicalTrial, pk=pk)
    except Http404:
        request.session["error_message"] = "Clinical trial not found!"
        request.session["status_code"] = 404
        return redirect("error")

    try:
        user_affiliation: Affiliation = affiliation_getter(request=request)
    except PermissionDenied as e:
        request.session["error_message"] = str(e)
        request.session["status_code"] = 403
        return redirect("error")

    if user_affiliation != clinical_trial.affiliation:
        request.session["error_message"] = (
            "Your affiliation doesn't match the clinical trial's affiliation, so you lack permission!"
        )
        request.session["status_code"] = 403
        return redirect("error")

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
    try:
        clinical_trial: ClinicalTrial = get_object_or_404(ClinicalTrial, pk=pk)
    except Http404:
        request.session["error_message"] = "Clinical trial not found!"
        request.session["status_code"] = 404
        return redirect("error")

    try:
        user_affiliation: Affiliation = affiliation_getter(request=request)
    except PermissionDenied as e:
        request.session["error_message"] = str(e)
        request.session["status_code"] = 403
        return redirect("error")

    if user_affiliation != clinical_trial.affiliation:
        request.session["error_message"] = (
            "Your affiliation doesn't match the clinical trial's affiliation, so you lack permission!"
        )
        request.session["status_code"] = 403
        return redirect("error")

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
    try:
        user_affiliation: Affiliation = affiliation_getter(request=request)
    except PermissionDenied as e:
        request.session["error_message"] = str(e)
        request.session["status_code"] = 403
        return redirect("error")

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
    try:
        clinical_trial: ClinicalTrial = get_object_or_404(ClinicalTrial, pk=pk)
    except Http404:
        request.session["error_message"] = "Clinical trial not found!"
        request.session["status_code"] = 404
        return redirect("error")

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
    try:
        affiliation_variable: Affiliation = affiliation_getter(request=request)
    except PermissionDenied as e:
        request.session["error_message"] = str(e)
        request.session["status_code"] = 403
        return redirect("error")

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
    try:
        publication: Publication = get_object_or_404(Publication, pk=pk)
    except Http404:
        request.session["error_message"] = "Publication not found!"
        request.session["status_code"] = 404
        return redirect("error")

    try:
        user_affiliation: Affiliation = affiliation_getter(request=request)
    except PermissionDenied as e:
        request.session["error_message"] = str(e)
        request.session["status_code"] = 403
        return redirect("error")

    if user_affiliation != publication.affiliation:
        request.session["error_message"] = (
            "Your affiliation doesn't match the publication's affiliation, so you lack permission!"
        )
        request.session["status_code"] = 403
        return redirect("error")

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
    try:
        publication: Publication = get_object_or_404(Publication, pk=pk)
    except Http404:
        request.session["error_message"] = "Publication not found!"
        request.session["status_code"] = 404
        return redirect("error")

    try:
        user_affiliation: Affiliation = affiliation_getter(request=request)
    except PermissionDenied as e:
        request.session["error_message"] = str(e)
        request.session["status_code"] = 403
        return redirect("error")

    if user_affiliation != publication.affiliation:
        request.session["error_message"] = (
            "Your affiliation doesn't match the publication's affiliation, so you lack permission!"
        )
        request.session["status_code"] = 403
        return redirect("error")

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
    try:
        user_affiliation: Affiliation = affiliation_getter(request=request)
    except PermissionDenied as e:
        request.session["error_message"] = str(e)
        request.session["status_code"] = 403
        return redirect("error")

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
    try:
        publication: Publication = get_object_or_404(Publication, pk=pk)
    except Http404:
        request.session["error_message"] = "Publication not found!"
        request.session["status_code"] = 404
        return redirect("error")

    has_rights: bool = False
    logged: bool = False

    if request.user.is_authenticated:
        logged = True
        user_affiliation: Affiliation = request.user.userprofile.affiliation
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
        raise PermissionDenied("You do not have affiliation!")

    else:
        return affiliation_result
