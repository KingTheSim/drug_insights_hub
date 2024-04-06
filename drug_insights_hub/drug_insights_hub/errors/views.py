from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def error(request: HttpRequest) -> HttpResponse:
    error_message = request.session.pop("error_message", None)
    if error_message is None:
        error_message = "Permission denied."
    
    status = request.session.pop("status_code", None)
    if status is None:
        status = 404

    if request.user.is_authenticated:
        logged: bool = True
    else:
        logged: bool = False
    return render(
        request=request,
        template_name="errors/error.html",
        context={
            "error_message": error_message,
            "status": status,
            "logged": logged,
        },
        status=status,
    )
