
from alternative_views.base import View
from alternative_views.mixins.object import ObjectMixin

from core.models import Project


class ProjectMixin(ObjectMixin):
    template_name = 'project.html'
    model = Project


class ProjectView(View):
    project = ProjectMixin()
