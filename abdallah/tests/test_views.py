from django.test import TestCase
from django.core.urlresolvers import reverse
from abdallah import models


class ViewProjectTest(TestCase):
    def setUp(self):
        self.project = models.Project.objects.create(
            name='abdallah',
            url='https://github.com/ZuluPro/abdallah.git')
        self.url = reverse('project', args=[self.project.name])

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)


class ViewBuildTest(TestCase):
    def setUp(self):
        self.project = models.Project.objects.create(
            name='abdallah',
            url='https://github.com/ZuluPro/abdallah.git')
        self.build = models.Build.objects.create(project=self.project)
        self.url = reverse('build', args=[self.project.name, self.build.number])

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)


class ViewJobTest(TestCase):
    def setUp(self):
        self.project = models.Project.objects.create(
            name='abdallah',
            url='https://github.com/ZuluPro/abdallah.git')
        self.build = models.Build.objects.create(project=self.project)
        self.job = models.Job.objects.create(build=self.build)
        self.url = reverse('job', args=[self.project.name, self.build.number, self.job.number])

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
