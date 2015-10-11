from rest_framework.routers import DefaultRouter
from abdallah.rest import viewsets

router = DefaultRouter()
router.register(r'project', viewsets.ProjectViewSet)
router.register(r'build', viewsets.BuildViewSet)
router.register(r'job', viewsets.JobViewSet)
