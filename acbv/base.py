
import copy

from django.utils.decorators import classonlymethod
from functools import update_wrapper
from django.utils.datastructures import SortedDict
import logging


class Mixin(object):

    # Tracks each time a Field instance is created. Used to retain order.
    creation_counter = 0

    def __init__(self, *args, **kwargs):
        super(Mixin, self).__init__(*args, **kwargs)

        # Increase the creation counter, and save our local copy.
        self.creation_counter = Mixin.creation_counter
        Mixin.creation_counter += 1

    def contribute_to_view(self, request):
        return {}


def get_declared_mixins(bases, attrs):
    """
    Create a list of mixin instances from the passed in 'attrs', plus any
    similar mixin on the base classes (in 'bases').
    """
    mixins = [(mixin_name, attrs.pop(mixin_name)) for mixin_name, obj in attrs.items() if isinstance(obj, Mixin)]
    mixins.sort(key=lambda x: x[1].creation_counter)

    # If this class is subclassing another Form, add that Form's fields.
    # Note that we loop over the bases in *reverse*. This is necessary in
    # order to preserve the correct order of fields.
    for base in bases[::-1]:
        if hasattr(base, 'base_mixins'):
            mixins = base.base_mixins.items() + mixins

    return SortedDict(mixins)


class ViewMetaclass(type):
    '''
    A meta class the will gather the view's mixins
    '''
    def __new__(cls, name, bases, attrs):
        attrs['base_mixins'] = get_declared_mixins(bases, attrs)
        new_class = super(ViewMetaclass, cls).__new__(cls, name, bases, attrs)
        return new_class


class View(object):

    __metaclass__ = ViewMetaclass

    def __init__(self, *args, **kwargs):
        super(View, self).__init__(*args, **kwargs)
        self.mixins = copy.deepcopy(self.base_mixins)
        self.contributed = {}
        self.logger = logging.getLogger('acbv.View')

    def contribute_to_view(self, request):
        '''
        For each mixin, sets the context, calls the contribute_to_view and
        update the view context according to their return
        '''
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

    def dispatch(self, request):
        pass
