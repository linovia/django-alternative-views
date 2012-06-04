
from django.core.exceptions import ImproperlyConfigured
# from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect

from alternative_views.mixins import Mixin

from .detail import SingleObjectMixin
from .list import MultipleObjectMixin
from .edit import BaseCreateView, BaseUpdateView


class ObjectMixin(Mixin):
    model = None
    queryset = None

    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'

    template_name_prefix = None

    form = None

    HERITAGE_PER_MODE = {
        'list': MultipleObjectMixin,
        'detail': SingleObjectMixin,
        'new': BaseCreateView,
        'update': BaseUpdateView,
    }

    def as_mode(self, mode):
        """
        Live update the instance to make a different heritage according to the
        mode.
        """
        # Probably another solution would be to copy the current object's dict
        # and push it to the instanced Mixin
        super(ObjectMixin, self).as_mode(mode)
        if not mode in self.HERITAGE_PER_MODE:
            raise NotImplementedError('Unknown mode: %s' % mode)
        cls_name = "%s%s" % (mode.capitalize(), self.__class__.__name__)
        heritage = (self.__class__, self.HERITAGE_PER_MODE[mode])
        cls = type(cls_name, heritage, {})
        self.__class__ = cls

    def get_object_name(self, *args, **kwargs):
        """
        Return a short name for the object.
        """
        return self.context_object_name

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

    def get_context(self, request, context, permissions=None, **kwargs):
        """
        Builds a context for this mixin.
        """
        self.request = request
        context.update(super(ObjectMixin, self).get_context(
            request, context, permissions, **kwargs))
        return context

    def process(self, request, context, **kwargs):
        if self.mode == 'new' and self.form.is_valid():
            return HttpResponseRedirect(self.get_success_url())
        if self.mode == 'update' and self.form.is_valid():
            return HttpResponseRedirect(self.get_success_url())
        return super(ObjectMixin, self).process(request, context, **kwargs)
