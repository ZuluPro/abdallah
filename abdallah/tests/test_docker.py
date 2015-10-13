import docker
from django.test import TestCase
from abdallah import docker_utils


class GetDockerClientTest(TestCase):
    def test_func(self):
        client = docker_utils.get_docker_client()
        self.assertIsInstance(client, docker.Client)
