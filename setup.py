#!/usr/bin/env python
from setuptools import setup, find_packages
import abdallah


def get_requirements():
    return open('requirements.txt').read().splitlines()


def get_test_requirements():
    return open('requirements-tests.txt').read().splitlines()


setup(
    name='abdallah',
    version=abdallah.__version__,
    description=abdallah.__doc__,
    author=abdallah.__author__,
    author_email=abdallah.__email__,
    install_requires=get_requirements(),
    tests_require=get_test_requirements(),
    license='BSD',
    url='https://github.com/django-dbbackup/django-dbbackup',
    keywords=['django', 'continuous integration', 'test'],
    packages=find_packages(exclude=['tests.runtests.main']),
    test_suite='tests.runtests.main',
    classifiers=[
        'Environment :: Web Environment',
        'Environment :: Console',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
