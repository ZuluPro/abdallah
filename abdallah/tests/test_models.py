import mock
from django.test import TestCase
from abdallah import models


class ProjectModelTest(TestCase):
    def setUp(self):
        self.project = models.Project.objects.create(
            name='abdallah',
            url='https://github.com/ZuluPro/abdallah.git')

    def test_create(self):
        pass

    @mock.patch('docker.Client.create_container', return_value={})
    @mock.patch('docker.Client.start', return_value=None)
    def test_launch_build(self, *args):
        self.project.launch_build()


class BuildModelTest(TestCase):
    def setUp(self):
        self.project = models.Project.objects.create(
            name='abdallah',
            url='https://github.com/ZuluPro/abdallah.git')

    def test_create(self):
        build = models.Build.objects.create(project=self.project)
        self.assertEqual(build.number, 1)


class JobModelTest(TestCase):
    def setUp(self):
        self.project = models.Project.objects.create(
            name='abdallah',
            url='https://github.com/ZuluPro/abdallah.git')
        self.build = models.Build.objects.create(project=self.project)

    def test_create(self):
        job = models.Job.objects.create(build=self.build)
        self.assertEqual(job.number, 1)
