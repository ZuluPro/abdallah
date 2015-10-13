import mock
from django.test import TestCase
from abdallah.build import run_build, run_job
from abdallah import models


class RunBuildTest(TestCase):
    def setUp(self):
        self.project = models.Project.objects.create(
            name='abdallah',
            url='https://github.com/ZuluPro/abdallah.git')

    @mock.patch('docker.Client.create_container', return_value={})
    @mock.patch('docker.Client.start')
    def test_func(self, *args):
        build = run_build(self.project)
        self.assertEqual(build.project, self.project)


class RunJobTest(TestCase):
    def setUp(self):
        self.project = models.Project.objects.create(
            name='abdallah',
            url='https://github.com/ZuluPro/abdallah.git')
        self.build = models.Build.objects.create(project=self.project, commit='master')
        self.job = models.Job.objects.create(build=self.build)

    @mock.patch('docker.Client.create_container', return_value={})
    @mock.patch('docker.Client.start')
    def test_func(self, *args):
        run_job(self.job, self.build.get_jobs_configuration()[0])
