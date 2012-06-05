"""

"""

from alternative_views.base import View
from alternative_views.mixins.object import ObjectMixin
from demo.core.models import Project, Milestone, Bug


class ProjectMixin(ObjectMixin):
    model = Project
    pk_url_kwarg = 'project_id'
    success_url = '/projects/'


class MilestoneMixin(ObjectMixin):
    model = Milestone
    pk_url_kwarg = 'milestone_id'
    success_url = '/milestones/'

    def get_queryset(self):
        return Milestone.objects.filter(self.project)


class BugMixin(ObjectMixin):
    model = Bug
    pk_url_kwarg = 'bug_id'

    def get_queryset(self):
        # Limits the bugs to the current project's ones
        qs = Bug.objects.filter(project=self.project)
        if hasattr(self, 'milestone'):
            qs = qs.filter(milestone=self.milestone)
        return qs


class ProjectView(View):
    project = ProjectMixin()


class BugView(ProjectView):
    # Automatically inherit mixins from ProjectView
    bug = BugMixin()
