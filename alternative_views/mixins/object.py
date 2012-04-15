
from django.core.exceptions import ImproperlyConfigured

from alternative_views.mixins import Mixin


class ObjectMixin(Mixin):
    model = None
    queryset = None

    template_name_prefix = None

    def get_model_name(self):
        return self.model._meta.object_name.lower()

    def get_template_names(self):
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
                self.mode
            ))

        if hasattr(self, 'model') and hasattr(self.model, '_meta'):
            names.append("%s/%s_%s.html" % (
                self.model._meta.app_label,
                self.get_model_name(),
                self.mode
            ))
        return names

    def get_queryset(self):
        """
        Get the queryset to look an object up against. May not be called if
        `get_object` is overridden.
        """
        if self.queryset is None:
            if self.model:
                return self.model._default_manager.all()
            else:
                raise ImproperlyConfigured(
                    u"%(cls)s is missing a queryset. Define "
                    u"%(cls)s.model, %(cls)s.queryset, or override "
                    u"%(cls)s.get_object()." % {
                        'cls': self.__class__.__name__
                    })
        return self.queryset._clone()

    def get_object(self):
        obj = None
        return obj

    def get_context(self, request, context):
        context = super(ObjectMixin, self).get_context(request, context)
        if self.mode == 'list':
            context_name = '%s_list' % self.get_model_name()
            context[context_name] = self.get_queryset().all()
        elif self.mode == 'detail':
            context_name = '%s' % self.get_model_name()
            context[context_name] = self.get_object()
        else:
            raise NotImplementedError('Unimplemented mode: %s' % self.mode)
        return context
