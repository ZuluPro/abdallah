import mock
from rest_framework.test import APITestCase as TestCase
from rest_framework.reverse import reverse
from abdallah import models


class ViewSetProjectTest(TestCase):
    def setUp(self):
        self.project = models.Project.objects.create(
            name='abdallah',
            url='https://github.com/ZuluPro/abdallah.git')

    def test_get(self):
        url = reverse('api_v1:project-detail', args=[self.project.id])
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_list(self):
        url = reverse('api_v1:project-list')
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    @mock.patch('docker.Client.create_container', return_value={})
    @mock.patch('docker.Client.start', return_value=None)
    def test_run_build(self, *args):
        url = reverse('api_v1:project-run-build', args=[self.project.id])
        response = self.client.post(url)
        self.assertEqual(200, response.status_code)


class ViewSetBuildTest(TestCase):
    def setUp(self):
        self.project = models.Project.objects.create(
            name='abdallah',
            url='https://github.com/ZuluPro/abdallah.git')
        self.build = models.Build.objects.create(project=self.project)

    def test_get(self):
        url = reverse('api_v1:build-detail', args=[self.build.id])
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_list(self):
        url = reverse('api_v1:build-list')
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)


class ViewSetJobTest(TestCase):
    def setUp(self):
        self.project = models.Project.objects.create(
            name='abdallah',
            url='https://github.com/ZuluPro/abdallah.git')
        self.build = models.Build.objects.create(project=self.project)
        self.job = models.Job.objects.create(build=self.build)

    def test_get(self):
        url = reverse('api_v1:job-detail', args=[self.job.id])
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_list(self):
        url = reverse('api_v1:job-list')
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    @mock.patch('docker.Client.logs', return_value='FOO-BAR')
    def test_logs(self, *args):
        url = reverse('api_v1:job-logs', args=[self.job.id])
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
