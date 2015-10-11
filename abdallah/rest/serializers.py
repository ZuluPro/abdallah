from rest_framework import serializers
from abdallah.models import Project, Build, Job


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project


class BuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Build


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
