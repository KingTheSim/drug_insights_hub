from typing import Type

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.paginator import Page, Paginator
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from drug_insights_hub.research.models import ClinicalTrial, Drug, Publication


def index(request: HttpRequest) -> HttpResponse:
    user_type: Type[User] = get_user_model()
    users_count: int = user_type.objects.count()

    publications: QuerySet[Publication] = Publication.objects.order_by(
        "publication_date"
    ).all()
    publications_count: int = publications.count()

    clinical_trial_count: int = ClinicalTrial.objects.count()

    drugs_count: int = Drug.objects.count()

    per_page: int = 10
    paginator: Paginator = Paginator(publications, per_page=per_page)
    page_number: int = request.GET.get("page")
    page_obj: Page = paginator.get_page(page_number)

    if request.user.is_authenticated:
        logged = True
    else:
        logged = False

    return render(
        request=request,
        template_name="core/index.html",
        context={
            "page_obj": page_obj,
            "logged": logged,
            "users_count": users_count,
            "publications_count": publications_count,
            "clinical_trials_count": clinical_trial_count,
            "drugs_count": drugs_count,
        },
    )
