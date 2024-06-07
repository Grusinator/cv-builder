from django.shortcuts import render


def show_content(request):
    return render(request, 'base_cv_content.html')