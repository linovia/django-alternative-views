
import copy

from functools import update_wrapper

from django.utils.decorators import classonlymethod
from django.utils.datastructures import SortedDict
from django import http

from alternative_views.mixins import Mixin

from django.utils.log import getLogger
logger = getLogger('django.request')


def get_declared_mixins(bases, attrs):
    """
    Create a list of mixin instances from the passed in 'attrs', plus any
    similar mixin on the base classes (in 'bases').
    """
    mixins = [(mixin_name, attrs.pop(mixin_name))
        for mixin_name, obj in attrs.items() if isinstance(obj, Mixin)]
    mixins.sort(key=lambda x: x[1].creation_counter)

    # If this class is subclassing another Form, add that Form's fields.
    # Note that we loop over the bases in *reverse*. This is necessary in
    # order to preserve the correct order of fields.
    for base in bases[::-1]:
        if hasattr(base, 'base_mixins'):
            mixins = base.base_mixins.items() + mixins

    return SortedDict(mixins)


class ViewMetaclass(type):
    """
    A meta class the will gather the view's mixins
    """
    def __new__(cls, name, bases, attrs):
        attrs['base_mixins'] = get_declared_mixins(bases, attrs)
        new_class = super(ViewMetaclass, cls).__new__(cls, name, bases, attrs)
        return new_class


class View(object):
    """
    Container class for the mixins. It dispatch the requests depending on what
    mixins are able to do.
    Huge parts are taken from django.views.generic.base.View as they have
    similar roles.
    """

    __metaclass__ = ViewMetaclass

    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options', 'trace']
    mode = None

    def __init__(self, *args, **kwargs):
        self.mixins = copy.deepcopy(self.base_mixins)
        self.contributed = {}
        self.mode = kwargs.get('mode', None)
        self.context = {}

    def contribute_to_view(self, request):
        """
        For each mixin, sets the context, calls the contribute_to_view and
        update the view context according to their return
        """
        for name, mixin in self.mixins.iteritems():
            for key, value in self.contributed.iteritems():
                if hasattr(mixin, key):
                    self.logger.warning('Overriding %s in %s.' % (key, name))
                setattr(mixin, key, value)
            contribution = mixin.contribute_to_view(request)
            self.contributed.update(contribution)

    @classonlymethod
    def as_view(cls, **initkwargs):
        """
        Main entry point for a request-response process.
        """
        # sanitize keyword arguments
        for key in initkwargs:
            if key in cls.http_method_names:
                raise TypeError(u"You tried to pass in the %s method name as a "
                                u"keyword argument to %s(). Don't do that."
                                % (key, cls.__name__))
            if not hasattr(cls, key):
                raise TypeError(u"%s() received an invalid keyword %r" % (
                    cls.__name__, key))

        def view(request, *args, **kwargs):
            self = cls(**initkwargs)
            return self.dispatch(request, *args, **kwargs)

        # take name and docstring from class
        update_wrapper(view, cls, updated=())

        # and possible attributes set by decorators
        # like csrf_exempt from dispatch
        update_wrapper(view, cls.dispatch, assigned=())
        return view

    def find_http_method(self, request):
        """
        Searches for a mixin that can respond to the request.
        Search order is reversed as we expect latest mixins to be more
        specialized than the firsts.
        """
        for name, mixin in reversed(list(self.mixins.iteritems())):
            if mixin.can_process(request):
                return getattr(mixin, 'process')
        return self.http_method_not_allowed

    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        self.context = {}
        for mixin in self.mixins.values():
            self.context = mixin.get_context(request, self.context)

        if request.method.lower() in self.http_method_names:
            handler = self.find_http_method(request)
        else:
            handler = self.http_method_not_allowed
        self.request = request
        self.args = args
        self.kwargs = kwargs
        return handler(request, self.context, *args, **kwargs)

    def http_method_not_allowed(self, request, context, *args, **kwargs):
        allowed_methods = [m for m in self.http_method_names if hasattr(self, m)]
        logger.warning(
            'Method Not Allowed (%s): %s' % (request.method, request.path),
            extra={
                'status_code': 405,
                'request': self.request
            }
        )
        return http.HttpResponseNotAllowed(allowed_methods)
