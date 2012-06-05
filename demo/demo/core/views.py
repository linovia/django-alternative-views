"""
Bug tracker views.
"""

from alternative_views.base import View
from alternative_views.mixins.object import ObjectMixin
from demo.core.models import Project, Milestone, Bug


class ProjectMixin(ObjectMixin):
    model = Project
    pk_url_kwarg = 'project_id'
    success_url = '/projects/'

    def get_queryset(self):
        return Project.objects.filter(members=self.request.user.id)


class MilestoneMixin(ObjectMixin):
    model = Milestone
    pk_url_kwarg = 'milestone_id'
    success_url = '/milestones/'

    def get_queryset(self):
        return Milestone.objects.filter(project=self.project)


class BugMixin(ObjectMixin):
    model = Bug
    pk_url_kwarg = 'bug_id'
    success_url = '/bugs/'

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
