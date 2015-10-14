from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import ugettext as _
from abdallah.models import Project


def project(request, name):
    import time; time.sleep(3)
    project = get_object_or_404(Project.objects.filter(name=name))
    return render(request, 'abdallah/project.html', {
        'title': str(project),
        'projects': Project.objects.all(),
        'project': project,
        'builds': project.build_set.order_by('-number'),
    })


def run_build(request, name):
    project = get_object_or_404(Project.objects.filter(name=name))
    build = project.launch_build(request.POST.get('commit', 'master'))
    messages.info(request, _('Build launched'))
    return redirect(build.get_absolute_url())


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
