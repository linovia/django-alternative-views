
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext as _

from alternative_views.mixins import Mixin

from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin


class AlternativeSingleObjectMixin(SingleObjectMixin):
    def get_context_data(self, **kwargs):
        context = {}
        obj = kwargs.pop('object')
        context_object_name = self.get_context_object_name(obj)
        if context_object_name:
            context[context_object_name] = obj
        context.update(kwargs)
        return context


class AlternativeMultipleObjectMixin(MultipleObjectMixin):
    pass


class ObjectMixin(Mixin,
        AlternativeSingleObjectMixin,
        AlternativeMultipleObjectMixin):

    instance_name = None
    model = None
    queryset = None

    template_name_prefix = None

    def get_object_name(self, *args, **kwargs):
        """
        Return a short name for the object.
        """
        return self.instance_name

    def get_context_object_name(self, *args, **kwargs):
        """
        Returns the instance name.
        Overrides the function from django's generic views.
        """
        name = self.get_object_name(*args, **kwargs)
        if self.mode == 'list':
            return '%s_list' % (name,)
        return name

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
                self.get_object_name(),
                self.mode
            ))
        return names

    def get_context(self, request, context, permissions, **kwargs):
        """
        Builds a context for this mixin.
        """
        context = super(ObjectMixin, self).get_context(
            request, context, permissions, **kwargs)
        local_context = {}

        if self.mode == 'list':
            local_context = AlternativeMultipleObjectMixin.get_context_data(
                self, object_list=self.get_queryset())
            # Sanitize the context names
            del local_context['object_list']

        elif self.mode == 'detail':
            local_context = AlternativeSingleObjectMixin.get_context_data(
                self, object=self.get_object())
        else:
            raise NotImplementedError('Unimplemented mode: %s' % self.mode)

        context.update(local_context)
        return context
