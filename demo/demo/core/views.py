"""

"""

from alternative_views.base import View
from alternative_views.mixins.object import ObjectMixin
from demo.core.models import Project, Milestone, Bug


class ProjectMixin(ObjectMixin):
    model = Project
    pk_url_kwarg = 'project_id'


class BugMixin(ObjectMixin):
    model = Bug
    pk_url_kwarg = 'bug_id'

    def get_queryset(self):
        # Limits the bugs to the current project's ones
        return Bug.objects.filter(self.project)


class ProjectView(View):
    project = ProjectMixin()


class BugView(ProjectView):
    # Automatically inherit mixins from ProjectView
    bug = BugMixin()
