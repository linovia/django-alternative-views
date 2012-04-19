
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.http import Http404
from django.utils.translation import ugettext as _

from alternative_views.mixins import Mixin


class SingleObjectMixin(Mixin):

    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'

    def get_slug_field(self):
        """
        Get the name of a slug field to be used to look up by slug.
        """
        return self.slug_field

    def get_object(self, request):
        queryset = self.queryset
        if queryset is None:
            queryset = self.get_queryset()

        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        # Next, try looking up by slug.
        elif slug is not None:
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        # If none of those are defined, it's an error.
        else:
            raise AttributeError(u"Generic detail view %s must be called with "
                                 u"either an object pk or a slug."
                                 % self.__class__.__name__)

        try:
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(_(u"No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj


class ObjectMixin(SingleObjectMixin, Mixin):
    instance_name = None
    model = None
    queryset = None

    template_name_prefix = None

    def get_model_name(self):
        # return self.model._meta.object_name.lower()
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

    def get_context(self, request, context, permissions, **kwargs):
        context = super(ObjectMixin, self).get_context(
            request, context, permissions, **kwargs)
        if self.mode == 'list':
            context_name = '%s_list' % self.get_model_name()
            context[context_name] = self.get_queryset().all()
        elif self.mode == 'detail':
            context_name = '%s' % self.get_model_name()
            context[context_name] = self.get_object(request)
        else:
            raise NotImplementedError('Unimplemented mode: %s' % self.mode)
        return context
