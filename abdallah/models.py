import yaml
from docker.errors import NotFound
from requests.exceptions import ConnectionError
from django.db import models
from django.utils.translation import ugettext as _
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import six
from rest_framework.reverse import reverse
from abdallah.build import run_build
from abdallah import settings
from abdallah.docker_utils import get_docker_client

STATUS_CHOICES = (
    ('INI', _('Initialized')),
    ('STA', _('Started')),
    ('STO', _('Stopped')),
    ('PAS', _('Passed')),
    ('FAI', _('Failed')),
    ('ERR', _('Errored')),
)
CSS_CLASSES = {
    'PAS': 'success',
    'FAI': 'danger',
    'STO': 'default',
    'ERR': 'danger',
}

DEFAULT_CONFIGURATION = """python:
    - "2.7"
install:
    - pip install -r requirements.txt
    - pip install -r requirements-tests.txt
script:
    - python setup.py test"""


class Project(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    url = models.CharField(max_length=300, null=False, blank=False,
                           verbose_name=_("Git URL"))
    configuration = models.TextField(blank=True, default=DEFAULT_CONFIGURATION)

    class Meta:
        app_label = 'abdallah'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project', args=[self.name])

    def get_run_build_url(self):
        return reverse('project-run-build', args=[self.name])

    def launch_build(self, commit='master'):
        return run_build(self, commit='master')


class Build(models.Model):
    number = models.IntegerField(null=False, blank=False,
                                 verbose_name=_("Build number"))
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, null=False, default='STA')
    commit = models.CharField(max_length=54, null=False)
    configuration = models.TextField(blank=True)

    project = models.ForeignKey('abdallah.Project')
    date = models.DateTimeField(auto_now_add=True)
    elapsed_time = models.IntegerField(null=True, blank=False)

    class Meta:
        app_label = 'abdallah'
        unique_together = (('number', 'project'))

    def __str__(self):
        return "%s: #%s" % (self.project.name, self.number)

    def get_absolute_url(self):
        return reverse('build', args=[self.project.name, self.number])

    def get_css_class(self):
        return CSS_CLASSES.get(self.status, 'info')

    def get_jobs_configuration(self):
        raw_conf = self.configuration or self.project.configuration
        configuration = six.next(yaml.load_all(raw_conf))
        jobs = [
            {
                'commit': self.commit,
                'repository': self.project.url,
                'env': configuration.get('env', []),
                'install': configuration.get('install', []),
                'script': configuration['script'],
                'after_success': configuration.get('after_success', [])
            }
            for version in configuration['python']
        ]
        return jobs


@receiver(pre_save, sender=Build)
def pre_save_build(sender, instance, **kwars):
    if not instance.number:
        instance.number = Build.objects.filter(project=instance.project)\
                                       .count() + 1


class Job(models.Model):
    number = models.IntegerField(null=False, blank=False,
                                 verbose_name=_("Job number"))
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, null=False, default='STA')

    build = models.ForeignKey('abdallah.Build', null=False)
    date = models.DateTimeField(auto_now_add=True)
    elapsed_time = models.IntegerField(null=True, blank=False)

    class Meta:
        app_label = 'abdallah'
        unique_together = (('number', 'build'))

    def __str__(self):
        return "%s: #%s.%s" % (self.build.project.name, self.build.number,
                               self.number)

    def get_absolute_url(self):
        return reverse('job', args=[self.build.project.name, self.build.number, self.number])

    def get_css_class(self):
        return CSS_CLASSES.get(self.status, 'info')

    @property
    def full_url(self):
        url = '%s%s' % (settings.API_URL,
                        reverse('api_v1:job-detail', args=[self.pk]))
        return url

    @property
    def container_name(self):
        return "%s_%s_%s" % (self.build.project.id, self.build.number,
                             self.number)

    @property
    def logs(self):
        try:
            client = get_docker_client()
            return client.logs(self.container_name)
        except NotFound:
            return _("Logs no longer exist.")
        except ConnectionError:
            return _("Can't connect to Docker.")


@receiver(pre_save, sender=Job)
def pre_save_job(sender, instance, **kwars):
    if not instance.number:
        instance.number = Job.objects.filter(build=instance.build)\
                                     .count() + 1


@receiver(post_save, sender=Job)
def post_save_job(sender, instance, **kwars):
    related_jobs = instance.build.job_set.all()
    build_failed = related_jobs.filter(status='FAI').exists()
    if build_failed:
        instance.build.status = 'FAI'
        instance.build.save()
    if related_jobs.exists():
        if related_jobs.filter(status='PAS').count() == related_jobs.count():
            instance.build.status = 'PAS'
        if related_jobs.filter(status='FAI').exists():
            instance.build.status = 'FAI'
        if related_jobs.filter(status='ERR').exists():
            instance.build.status = 'ERR'
        instance.build.save()
