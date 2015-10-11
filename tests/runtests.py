#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings
from django.core.management import call_command

here = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(here)
sys.path[0:0] = [here, parent]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'tests/media')
INSTALLED_APPS = (
    'abdallah',
)
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3',
                         'NAME': '/tmp/abdallah-test-db.sqlite'}}
DOCKER_CONFIG = {
    'VERSION': os.environ.get('ABDALLAH_DOCKER_VERSION', '1.12')
}


settings.configure(
    ADMIN=('foo@bar'),
    MEDIA_ROOT=MEDIA_ROOT,
    MIDDLEWARE_CLASSES=(),
    INSTALLED_APPS=INSTALLED_APPS,
    DATABASES=DATABASES,
    ROOT_URLCONF='testapp.urls',
    SECRET_KEY="it's a secret to everyone",
    SITE_ID=1,
    BASE_DIR=BASE_DIR,
    ABDALLAH_DOCKER=DOCKER_CONFIG
)


def main():
    if django.VERSION >= (1, 7):
        django.setup()
    command_args = sys.argv[1:] or ['test', 'abdallah']
    call_command(*command_args)
    exit(0)

if __name__ == '__main__':
    main()
