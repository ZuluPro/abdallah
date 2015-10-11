from django.conf import settings

REPOS_DIR = getattr(settings, 'ABDALLAH_REPOS_DIR', None)

DOCKER = {
    'BASE_URL': None,
    'VERSION': None,
    'TIMEOUT': 30,
    'TLS': False
}
DOCKER.update(getattr(settings, 'ABDALLAH_DOCKER', {}))
API_URL = getattr(settings, 'ABDALLAH_API_URL', None)
