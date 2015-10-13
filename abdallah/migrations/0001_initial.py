# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Build',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(verbose_name='Build number')),
                ('status', models.CharField(max_length=3, choices=[(b'INI', 'Initialized'), (b'STA', 'Started'), (b'STO', 'Stopped'), (b'PAS', 'Passed'), (b'FAI', 'Failed')])),
                ('commit', models.CharField(max_length=54)),
                ('configuration', models.TextField(blank=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('elapsed_time', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(verbose_name='Job number')),
                ('status', models.CharField(max_length=3, choices=[(b'INI', 'Initialized'), (b'STA', 'Started'), (b'STO', 'Stopped'), (b'PAS', 'Passed'), (b'FAI', 'Failed')])),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('elapsed_time', models.IntegerField(null=True)),
                ('build', models.ForeignKey(to='abdallah.Build')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('url', models.CharField(max_length=300, verbose_name='Git URL')),
                ('configuration', models.TextField(default=b'python:\n    - "2.7"\ninstall:\n    - pip install -r requirements.txt\n    - pip install -r requirements-tests.txt\nscript:\n    - python setup.py test', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='build',
            name='project',
            field=models.ForeignKey(to='abdallah.Project'),
        ),
        migrations.AlterUniqueTogether(
            name='job',
            unique_together=set([('number', 'build')]),
        ),
        migrations.AlterUniqueTogether(
            name='build',
            unique_together=set([('number', 'project')]),
        ),
    ]
