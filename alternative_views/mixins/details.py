

from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils.translation import ugettext as _
from base import Mixin


class ObjectMixin(Mixin):
    model = None
    queryset = None
    slug_field = 'slug'
    context_object_name = None
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'

    def has_perm(self, user):
        return True

    def get_object(self, request, queryset=None):
        """
        Returns the object the view is displaying.

        By default this requires `self.queryset` and a `pk` or `slug` argument
        in the URLconf, but subclasses can override this to return any object.
        """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
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
            raise AttributeError(
                u"Generic detail view %s must be called with "
                u"either an object pk or a slug."
                % self.__class__.__name__)

        try:
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(_(u"No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})

        self.object = obj
        if not self.has_perm(request.user):
            raise PermissionDenied()
        return obj

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

"""
Model mixin
"""

from ..base import Mixin

# Methods:
# ['get', 'post', 'put', 'delete', 'head', 'options', 'trace']
METHODS_FOR_MODE = {
    'list': ['get'],
    'detail': ['get'],
    'update': ['get', 'post'],
    'delete': ['get', 'post'],
    'new': ['get', 'post'],
}


class ObjectDetailMixin(object):

    def contribute_to_view_detail(self, request):
        return {
            'objects': self.get_query_set().all()
        }

    def get_detail(self, request):
        return {
            'objects': self.get_query_set().all()
        }


class ModelMixin(Mixin):
    model = None
    queryset = None

    def get_query_set(self):
        if self.queryset:
            return self.queryset
        # Guess from model
        return self.model.objects

    def __init__(self, mode=None, **kwargs):
        super(ModelMixin, self).__init__(**kwargs)
        if mode not in METHODS_FOR_MODE:
            raise KeyError('Unknown mode: %s')
        self.mode = mode
        self.allowed_methods = METHODS_FOR_MODE[mode]

        contribute_to_view = getattr(self, 'contribute_to_view_%s' % (mode,))
        setattr(self, 'contribute_to_view', contribute_to_view)

        for method in self.allowed_methods:
            entry_point = getattr(self, '%s_%s' % (method, mode))
            setattr(self, method, entry_point)

        self.template_name_suffix = "_%s" % (mode,)

    # def get_template_names(self):
    #     """
    #     Return a list of template names to be used for the request. Must return
    #     a list. May not be called if get_template is overridden.
    #     """
    #     try:
    #         names = super(ModelMixin, self).get_template_names()
    #     except ImproperlyConfigured:
    #         # If template_name isn't specified, it's not a problem --
    #         # we just start with an empty list.
    #         names = []

    #     # The least-specific option is the default <app>/<model>_detail.html;
    #     # only use this if the object in question is a model.
    #     if hasattr(self.object, '_meta'):
    #         names.append("%s/%s%s.html" % (
    #             self.object._meta.app_label,
    #             self.object._meta.object_name.lower(),
    #             self.template_name_suffix
    #         ))
    #     elif hasattr(self, 'model') and hasattr(self.model, '_meta'):
    #         names.append("%s/%s%s.html" % (
    #             self.model._meta.app_label,
    #             self.model._meta.object_name.lower(),
    #             self.template_name_suffix
    #         ))
    #     return names

    # LIST
    def contribute_to_view_list(self, request):
        return {
            'objects': self.get_query_set().all()
        }

    def get_list(self, request):
        return {
            'objects': self.get_query_set().all()
        }
