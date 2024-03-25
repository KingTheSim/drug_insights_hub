from django.core.paginator import Page, Paginator
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from drug_insights_hub.research.models import Publication


def index(request: HttpRequest) -> HttpResponse:
    publications: QuerySet = Publication.objects.order_by("publication_date").all()
    per_page: int = 10
    paginator: Paginator = Paginator(publications, per_page=per_page)
    page_number: int = request.GET.get("page")
    page_obj: Page = paginator.get_page(page_number)
    return render(
        request=request,
        template_name="core/index.html",
        context={"page_obj": page_obj},
    )
