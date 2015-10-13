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
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'rest_framework'
)
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

)
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': (
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        )
    }
}]
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3',
                         'NAME': '/tmp/abdallah-test-db.sqlite'}}
DOCKER_CONFIG = {
    'VERSION': os.environ.get('ABDALLAH_DOCKER_VERSION', '1.12')
}
API_URL = os.environ.get('ABDALLAH_API_URL', '')


settings.configure(
    DEBUG=True,
    ADMIN=('foo@bar'),
    ALLOWED_HOSTS=['*'],
    MEDIA_ROOT=MEDIA_ROOT,
    INSTALLED_APPS=INSTALLED_APPS,
    MIDDLEWARE_CLASSES=MIDDLEWARE_CLASSES,
    TEMPLATES=TEMPLATES,
    DATABASES=DATABASES,
    ROOT_URLCONF='urls',
    SECRET_KEY="it's a secret to everyone",
    SITE_ID=1,
    STATIC_URL='/static/',
    BASE_DIR=BASE_DIR,
    ABDALLAH_DOCKER=DOCKER_CONFIG,
    ABDALLAH_API_URL=API_URL
)


def main():
    if django.VERSION >= (1, 7):
        django.setup()
    command_args = sys.argv[1:] or ['test', 'abdallah']
    call_command(*command_args)
    exit(0)

if __name__ == '__main__':
    main()
