
from django.core.exceptions import ImproperlyConfigured

from alternative_views.mixins import Mixin


class ObjectMixin(Mixin):
    model = None
    template_name_prefix = None

    def get_template_names(self, mode=None):
        """
        Return a list of template names to be used for the request. Must return
        a list. May not be called if get_template is overridden.
        """
        try:
            names = super(ObjectMixin, self).get_template_names()
        except ImproperlyConfigured:
            # If template_name isn't specified, it's not a problem --
            # we just start with an empty list.
            names = []

        if self.template_name_prefix:
            names.append("%s_%s.html" % (
                self.template_name_prefix,
                mode
            ))

        if hasattr(self, 'model') and hasattr(self.model, '_meta'):
            names.append("%s/%s_%s.html" % (
                self.model._meta.app_label,
                self.model._meta.object_name.lower(),
                mode
            ))
        return names
