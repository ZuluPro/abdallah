from django.shortcuts import render, get_object_or_404
from abdallah.models import Project


def project(request, name):
    project = get_object_or_404(Project.objects.filter(name=name))
    return render(request, 'abdallah/project.html', {
        'title': str(project),
        'projects': Project.objects.all(),
        'project': project,
        'builds': project.build_set.order_by('-number'),
    })


def build(request, name, build_number):
    project = get_object_or_404(Project.objects.filter(name=name))
    build = get_object_or_404(project.build_set.filter(number=build_number))
    return render(request, 'abdallah/build.html', {
        'title': str(build),
        'projects': Project.objects.all(),
        'build': build,
        'jobs': build.job_set.order_by('number')
    })


def job(request, name, build_number, job_number):
    project = get_object_or_404(Project.objects.filter(name=name))
    build = get_object_or_404(project.build_set.filter(number=build_number))
    job = get_object_or_404(build.job_set.filter(number=job_number))
    return render(request, 'abdallah/job.html', {
        'title': str(job),
        'projects': Project.objects.all(),
        'job': job
    })
