from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from abdallah.models import Project, Build, Job
from abdallah.rest import serializers


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    authentication_classes = ()

    @detail_route(methods=['post'])
    def run_build(self, request, pk=None):
        """Run a build for a project and a commit."""
        queryset = Project.objects.all()
        project = get_object_or_404(queryset, pk=pk)
        build = project.launch_build(commit=request.data.get('commit', 'master'))
        serializer = serializers.BuildSerializer(build)
        return Response(serializer.data)


class BuildViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Build.objects.all()
    serializer_class = serializers.BuildSerializer
    authentication_classes = ()


class JobViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Job.objects.all()
    serializer_class = serializers.JobSerializer
    authentication_classes = ()

    @detail_route(methods=['get'])
    def logs(self, request, pk=None):
        queryset = Job.objects.all()
        job = get_object_or_404(queryset, pk=pk)
        return Response(job.logs)
