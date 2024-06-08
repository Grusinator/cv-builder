from bokeh.embed import server_document
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def build_cv_panel(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    bokeh_script_url = request.build_absolute_uri()
    script = server_document(bokeh_script_url, arguments={"user_id": request.user.id})
    return render(request, "base.html", {"script": script})


def home_view(request):
    return render(request, "cv_build_home.html")
