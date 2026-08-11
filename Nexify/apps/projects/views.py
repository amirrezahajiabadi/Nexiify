from django.shortcuts import render

from .models import Project


def project_list(request):
    projects = Project.objects.filter(is_published=True)
    return render(request, "projects.html", {"projects": projects})
