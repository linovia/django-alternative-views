"""
Tests the Mixins permissions.
"""

from django.core.exceptions import ImproperlyConfigured
from  django.core.exceptions import PermissionDenied

from django.test import RequestFactory
from django.test import TestCase

from alternative_views.mixins import Mixin
from alternative_views.base import View


class MyMixin1(Mixin):
    allowed_methods = ['get']


class MyMixin2(Mixin):
    pass


class PermissionMixin(Mixin):

    RESPONSE_CODE = False

    def authorization(self, request, context, **kwargs):
        return self.RESPONSE_CODE


class PermissionView(View):
    mixin1 = MyMixin1()
    permission = PermissionMixin()
    mixin2 = MyMixin2()


class PermissionView2(View):
    permission1 = PermissionMixin()
    permission2 = PermissionMixin()


class TestAuthorization(TestCase):

    def test_denied_if_a_mixin_denies_it(self):
        view = PermissionView(mode='detail')
        self.assertEqual(view.default_security, 'allow')
        rf = RequestFactory()
        request = rf.get('/')

        view.mixins['permission'].RESPONSE_CODE = False
        with self.assertRaises(PermissionDenied):
            view.dispatch(request)

    def test_authorized_if_a_mixin_authorize_it(self):
        view = PermissionView(mode='detail')
        self.assertEqual(view.default_security, 'allow')
        rf = RequestFactory()
        request = rf.get('/')

        # we get ImproperlyConfigured because we have no template name
        view.mixins['permission'].RESPONSE_CODE = True
        with self.assertRaises(ImproperlyConfigured):
            view.dispatch(request)

    def test_authorized_if_no_mixin_respond_and_policy_is_allow(self):
        view = PermissionView(mode='detail')
        view.default_security = 'allow'
        rf = RequestFactory()
        request = rf.get('/')

        # we get ImproperlyConfigured because we have no template name
        view.mixins['permission'].RESPONSE_CODE = None
        with self.assertRaises(ImproperlyConfigured):
            view.dispatch(request)

    def test_authorized_if_no_mixin_respond_and_policy_is_deny(self):
        view = PermissionView(mode='detail')
        view.default_security = 'deny'
        rf = RequestFactory()
        request = rf.get('/')

        # we get ImproperlyConfigured because we have no template name
        view.mixins['permission'].RESPONSE_CODE = None
        with self.assertRaises(PermissionDenied):
            view.dispatch(request)
