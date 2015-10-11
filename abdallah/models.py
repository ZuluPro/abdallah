import yaml
from django.db import models
from django.utils.translation import ugettext as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from abdallah.build import run_build

STATUS_CHOICES = (
    ('STA', _('Started')),
    ('PEN', _('Pending')),
    ('STO', _('Stopped')),
    ('PAS', _('Passed')),
    ('FAI', _('Failed')),
)


class Project(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=300)
    configuration = models.TextField(blank=True)

    class Meta:
        app_label = 'abdallah'

    def __str__(self):
        return self.name

    def launch_build(self, commit='master'):
        run_build(self, commit='master')


class Build(models.Model):
    number = models.IntegerField(null=False, blank=False)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, null=False)
    commit = models.CharField(max_length=54, null=False)
    configuration = models.TextField(blank=True)

    project = models.ForeignKey('abdallah.Project')
    date = models.DateTimeField(auto_now_add=True)
    elapsed_time = models.IntegerField(null=True, blank=False)

    class Meta:
        app_label = 'abdallah'

    def __str__(self):
        return "%s: #%s" % (self.project.name, self.number)

    def get_jobs_configuration(self):
        raw_conf = self.configuration or self.project.configuration
        configuration = yaml.load_all(raw_conf).next()
        jobs = [
            {
                'commit': self.commit,
                'repository': self.project.url,
                'env': configuration['env'],
                'install': configuration['install'],
                'script': configuration['script'],
                'after_success': configuration['after_success']
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
    number = models.IntegerField(null=False, blank=False)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, null=False)

    build = models.ForeignKey('abdallah.Build', null=False)
    date = models.DateTimeField(auto_now_add=True)
    elapsed_time = models.IntegerField(null=True, blank=False)

    class Meta:
        app_label = 'abdallah'

    def __str__(self):
        return "%s: #%s.%s" % (self.build.project.name, self.build.number,
                               self.number)

    @property
    def container_name(self):
        return "%s_%s_%s" % (self.build.project.id, self.build.number,
                             self.number)


@receiver(pre_save, sender=Job)
def pre_save_job(sender, instance, **kwars):
    if not instance.number:
        instance.number = Job.objects.filter(build=instance.build)\
                                     .count() + 1
