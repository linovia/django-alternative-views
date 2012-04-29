
from django.core.exceptions import ImproperlyConfigured
# from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect

from alternative_views.mixins import Mixin

from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.edit import ModelFormMixin


class AlternativeSingleObjectMixin(SingleObjectMixin):
    """
    The detail mixin
    """
    def get_context_object_name(self, *args, **kwargs):
        return self.get_object_name(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {}
        obj = kwargs.pop('object')
        context_object_name = self.get_context_object_name(obj)
        if context_object_name:
            context[context_object_name] = obj
        context.update(kwargs)
        return context

    def get_context(self, request, context, permissions, **kwargs):
        """
        Builds a context for this mixin.
        """
        self.object = self.get_object()
        ctx = self.get_context_data(object=self.get_object())
        context.update(ctx)
        return context


class AlternativeMultipleObjectMixin(MultipleObjectMixin):
    def get_context_object_name(self, *args, **kwargs):
        return '%s_list' % self.get_object_name(*args, **kwargs)

    def get_context(self, request, context, permissions, **kwargs):
        ctx = super(AlternativeMultipleObjectMixin, self).get_context_data(
            object_list=self.get_queryset())
        # Sanitize the context names
        del ctx['object_list']
        context.update(ctx)
        return context


class AlternativeModelFormMixin(ModelFormMixin):
    def get_context_object_name(self, *args, **kwargs):
        return self.get_object_name(*args, **kwargs)

    def get_context(self, request, context, permissions, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        self.form = form
        if request.method in ('POST', 'PUT'):
            if form.is_valid():
                local_context = self.form_valid(form)
            else:
                local_context = self.form_invalid(form)
        else:
            local_context = AlternativeModelFormMixin.get_context_data(self, form=form)
            local_context['%s_form' % self.get_object_name()] = local_context['form']
            del local_context['form']
        context.update(local_context)
        return context

    def form_invalid(self, form):
        return self.get_context_data(form=form)

    def form_valid(self, form):
        self.object = form.save()
        return


class ObjectMixin(Mixin):
    instance_name = None

    model = None
    queryset = None

    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'

    template_name_prefix = None

    form = None

    HERITAGE_PER_MODE = {
        'list': AlternativeMultipleObjectMixin,
        'detail': AlternativeSingleObjectMixin,
        'new': AlternativeModelFormMixin,
    }

    def as_mode(self, mode):
        """
        Live update the instance to make a different heritage according to the
        mode.
        """
        super(ObjectMixin, self).as_mode(mode)
        if mode in self.HERITAGE_PER_MODE:
            cls_name = "%s%s" % (mode.capitalize(), self.__class__.__name__)
            heritage = (self.__class__, self.HERITAGE_PER_MODE[mode])
            cls = type(cls_name, heritage, {})
            self.__class__ = cls

    def get_object_name(self, *args, **kwargs):
        """
        Return a short name for the object.
        """
        return self.instance_name

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
        if self.mode == 'new':
            if self.form.is_valid():
                return HttpResponseRedirect(self.get_success_url())
        return super(ObjectMixin, self).process(request, context, **kwargs)
