
from alternative_views.base import View
from alternative_views.mixins import Mixin

from core.models import Project


class ProjectMixin(Mixin):
    template_name = 'project.html'
    model = Project


class ProjectView(View):
    project = ProjectMixin()
