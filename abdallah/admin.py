from django.contrib import admin
from abdallah.models import Project, Build, Job


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    list_display_links = ('name',)


class BuildAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status')
    list_display_links = ('__str__',)
    list_filter = ('project', 'status')
    readonly_fields = ('status', 'elapsed_time', 'number', 'commit', 'project')


class JobAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status')
    list_display_links = ('__str__',)
    list_filter = ('build__project', 'status')
    readonly_fields = ('status', 'elapsed_time', 'number', 'build')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Build, BuildAdmin)
admin.site.register(Job, JobAdmin)
