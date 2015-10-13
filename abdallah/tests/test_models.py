import mock
from docker.errors import NotFound
from django.test import TestCase
from django.utils import six
from abdallah import models


class ProjectModelTest(TestCase):
    def setUp(self):
        self.project = models.Project.objects.create(
            name='abdallah',
            url='https://github.com/ZuluPro/abdallah.git')

    def test_create(self):
        pass

    def test_get_absolute_url(self):
        url = self.project.get_absolute_url()
        self.assertIsInstance(url, six.string_types)

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

    def test_get_absolute_url(self):
        build = models.Build.objects.create(project=self.project)
        url = build.get_absolute_url()
        self.assertIsInstance(url, six.string_types)

    def test_get_css_class(self):
        build = models.Build.objects.create(project=self.project)
        build.get_css_class()


class JobModelTest(TestCase):
    def setUp(self):
        self.project = models.Project.objects.create(
            name='abdallah',
            url='https://github.com/ZuluPro/abdallah.git')
        self.build = models.Build.objects.create(project=self.project)

    def test_create(self):
        job = models.Job.objects.create(build=self.build)
        self.assertEqual(job.number, 1)

    def test_get_absolute_url(self):
        job = models.Job.objects.create(build=self.build)
        url = job.get_absolute_url()
        self.assertIsInstance(url, six.string_types)

    def test_get_css_class(self):
        job = models.Job.objects.create(build=self.build)
        suffix = job.get_css_class()
        self.assertIsInstance(suffix, six.string_types)

    def test_container_name(self):
        job = models.Job.objects.create(build=self.build)
        self.assertIsInstance(job.container_name, six.string_types)

    @mock.patch('docker.Client.logs', return_value='FOO-BAR')
    def test_logs(self, *args):
        job = models.Job.objects.create(build=self.build)
        logs = job.logs
        self.assertIsInstance(logs, six.string_types)
        self.assertEqual(logs, 'FOO-BAR')

    @mock.patch('docker.Client.logs', side_effect=NotFound('foo', mock.MagicMock()))
    def test_logs_not_found_container(self, *args):
        job = models.Job.objects.create(build=self.build)
        logs = job.logs
        self.assertIsInstance(logs, six.string_types)
