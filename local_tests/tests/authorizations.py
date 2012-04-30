"""
Tests the Mixins permissions.
"""

from django.core.exceptions import ImproperlyConfigured

from django.test import RequestFactory
from django.test import TestCase

from alternative_views.mixins import Mixin
from alternative_views.base import View


class MyMixin1(Mixin):
    allowed_methods = ['get']


class MyMixin2(Mixin):
    pass


class ForbiddenMixin(Mixin):

    RESPONSE_CODE = False

    def authorization(self, request, context, **kwargs):
        return self.RESPONSE_CODE


class ForbiddenView(View):
    mixin1 = MyMixin1()
    forbidden = ForbiddenMixin()
    mixin2 = MyMixin2()


class TestAuthorization(TestCase):

    def test_authorizations(self):
        from  django.core.exceptions import PermissionDenied
        view = ForbiddenView(mode='detail')
        rf = RequestFactory()
        request = rf.get('/')
        with self.assertRaises(PermissionDenied):
            view.dispatch(request)

        view.mixins['forbidden'].RESPONSE_CODE = True
        with self.assertRaises(ImproperlyConfigured):
            view.dispatch(request)

        view.mixins['forbidden'].RESPONSE_CODE = None
        with self.assertRaises(ImproperlyConfigured):
            view.dispatch(request)
