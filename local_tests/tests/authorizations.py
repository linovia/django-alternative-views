"""

"""

from django.test import RequestFactory

from django.test import TestCase

from alternative_views.mixins import Mixin
from alternative_views.base import View


class MyMixin1(Mixin):
    allowed_methods = ['get']


class MyMixin2(Mixin):
    pass


class ForbiddenMixin(Mixin):
    def authorization(self, request, context, **kwargs):
        return False


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
