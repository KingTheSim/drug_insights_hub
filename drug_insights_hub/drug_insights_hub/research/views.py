from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required, user_passes_test
from drug_insights_hub.research.models import Drug
from drug_insights_hub.research.forms import DrugCreationForm, DrugUpdateForm

   
@login_required
def drug_creation(request: HttpRequest) -> HttpResponse:
    form = DrugCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("index")
    else:
        return render(request, "research/drugs/drug_creation.html", {"form": form})

@login_required
def drug_update(request: HttpRequest, pk: int) -> HttpResponse:
    drug = get_object_or_404(Drug, pk=pk)

    user_affiliation = request.user.userprofile.affiliation

    if user_affiliation != drug.affiliated_institution:
        return HttpResponseForbidden("You do not have permission to update this drug.")
    
    form = DrugUpdateForm(request.POST or None, instance=drug)
    if form.is_valid():
        form.save()
        return redirect("index")
    else:
        return render(request, "research/drugs/drug_update.html", {"form": form, "drug": drug})