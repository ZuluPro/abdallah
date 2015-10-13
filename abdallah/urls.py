from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^project/(?P<name>[^/.]+)$', 'abdallah.views.project', name="project"),
    url(r'^project/(?P<name>[^/.]+)/build/(?P<build_number>[^/.]+)$', 'abdallah.views.build', name="build"),
    url(r'^project/(?P<name>[^/.]+)/build/(?P<build_number>[^/.]+)/(?P<job_number>[^/.]+)$', 'abdallah.views.job', name="job"),
)
