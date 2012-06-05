"""
Bug tracker views.
"""

from alternative_views.base import View
from alternative_views.mixins.object import ObjectMixin
from demo.core.models import Project, Milestone, Bug
from django.core.urlresolvers import reverse


class ProjectMixin(ObjectMixin):
    model = Project
    pk_url_kwarg = 'project_id'

    def get_success_url(self):
        return reverse('projects')

    def get_queryset(self):
        return Project.objects.filter(members=self.request.user.id)


class MilestoneMixin(ObjectMixin):
    model = Milestone
    pk_url_kwarg = 'milestone_id'

    def get_success_url(self):
        return reverse('milestones')

    def get_queryset(self):
        return Milestone.objects.filter(project=self.project)


class BugMixin(ObjectMixin):
    model = Bug
    pk_url_kwarg = 'bug_id'

    def get_success_url(self):
        return reverse('bugs', kwargs={'project_id': self.project.id})

    def get_queryset(self):
        # Limits the bugs to the current project's ones
        # and possibly the milestone if we have one
        qs = Bug.objects.filter(project=self.project)
        if hasattr(self, 'milestone'):
            qs = qs.filter(milestone=self.milestone)
        return qs


class ProjectView(View):
    project = ProjectMixin(default_mode='detail')


class MilestoneView(ProjectView):
    milestone = MilestoneMixin(default_mode='detail')


class BugView(ProjectView):
    milestones = MilestoneMixin(mode='list')
    bug = BugMixin(default_mode='detail')


class BugMilestoneView(MilestoneView):
    bug = BugMixin(default_mode='detail')
