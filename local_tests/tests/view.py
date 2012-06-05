"""

"""
from django.test import RequestFactory

from django.test import TestCase

from alternative_views.base import View
from alternative_views.mixins import Mixin


class MyMixin1(Mixin):
    allowed_methods = ['get']


class ContextMixin(Mixin):
    def get_context(self, request, context, **kwargs):
        super(ContextMixin, self).get_context(request, context)
        context['updated_infos'] = True
        return context


class ContextMixin2(Mixin):
    template_name = 'demo.html'

    def get_context(self, request, context, **kwargs):
        super(ContextMixin2, self).get_context(request, context)
        context['context_mixin2_was_there'] = 'Some data'
        return context


class ContentView(View):
    mixin1 = MyMixin1()
    context1 = ContextMixin()
    context2 = ContextMixin2()


class TestViewResponse(TestCase):

    def test_context_updates(self):
        view = ContentView(mode='detail')
        rf = RequestFactory()
        request = rf.get('/')
        view.dispatch(request)
        expected_context = {
            'updated_infos': True,
            'context_mixin2_was_there': 'Some data',
        }
        self.assertEqual(view.context, expected_context)

    def test_view_returns_a_http_response(self):
        from django.http import HttpResponse
        view = ContentView(mode='detail')
        rf = RequestFactory()
        request = rf.get('/')
        response = view.dispatch(request)
        self.assertTrue(isinstance(response, HttpResponse))
        expected_context = {
            'updated_infos': True,
            'context_mixin2_was_there': 'Some data',
        }
        self.assertEqual(response.context_data, expected_context)

    def test_mixins_have_others_context(self):
        view = ContentView(mode='detail')
        rf = RequestFactory()
        request = rf.get('/')
        view.dispatch(request)
        self.assertTrue(hasattr(view.mixins['context2'], 'updated_infos'))
        self.assertEqual(view.mixins['context2'].updated_infos, True)
