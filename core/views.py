from django.shortcuts import render


def home_view(request):
    return render(request, "home.html")



"""


now ive put my static files inside the dir core/static/ fx core/static/assets/css/main.css

my static section in settings looks like this: 

STATIC_URL = "static/"

STATICFILES_DIRS = [bokehjsdir()]
STATIC_ROOT = BASE_DIR / 'staticfiles'

"""