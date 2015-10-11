from django.contrib import admin
from abdallah.models import Project, Build, Job


class ProjectAdmin(admin.ModelAdmin):
    pass


class BuildAdmin(admin.ModelAdmin):
    pass


class JobAdmin(admin.ModelAdmin):
    pass


admin.site.register(Project, ProjectAdmin)
admin.site.register(Build, BuildAdmin)
admin.site.register(Job, JobAdmin)
