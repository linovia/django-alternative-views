

from django.contrib import admin
from core.models import Project, Milestone


class ProjectAdmin(admin.ModelAdmin):
    pass


class MilestoneAdmin(admin.ModelAdmin):
    pass

admin.site.register(Project, ProjectAdmin)
admin.site.register(Milestone, MilestoneAdmin)
