
# from django.test import TestCase
from django.test import RequestFactory
from django import http
from django.db import models

from unittest2 import TestCase
# from mock import Mock
# import types
# import copy

from alternative_views.base import View
from alternative_views.mixins import Mixin
from alternative_views.mixins.object import ObjectMixin


class MyMixin1(Mixin):
    allowed_methods = ['get']


class MyMixin2(Mixin):
    pass


class ForbiddenMixin(Mixin):
    def authorization(self, request, context):
        return False


class ContextMixin(Mixin):
    def get_context(self, request, context):
        super(ContextMixin, self).get_context(request, context)
        context['updated_infos'] = True
        return context


class ContextMixin2(Mixin):
    template_name = 'demo.html'

    def get_context(self, request, context):
        super(ContextMixin2, self).get_context(request, context)
        context['context_mixin2_was_there'] = 'Some data'
        return context


class MyView1(View):
    mixin1 = MyMixin1()
    mixin2 = MyMixin2()


class MyView2(View):
    mixin2 = MyMixin2()
    mixin1 = MyMixin1()


class MySubView(MyView1):
    mixin3 = MyMixin1()


class ForbiddenView(View):
    mixin1 = MyMixin1()
    forbidden = ForbiddenMixin()
    mixin2 = MyMixin2()


class ContentView(View):
    mixin1 = MyMixin1()
    context1 = ContextMixin()
    context2 = ContextMixin2()


class TestMixins(TestCase):

    def test_two_Mixin_instances_have_different_creation_counter(self):
        mixin1 = MyMixin1()
        mixin2 = MyMixin2()
        mixin1b = MyMixin1()
        self.assertEqual(mixin1.creation_counter + 1, mixin2.creation_counter)
        self.assertEqual(mixin2.creation_counter + 1, mixin1b.creation_counter)


class TestView(TestCase):

    def test_base_mixins_is_an_sorted_dict(self):
        from django.utils.datastructures import SortedDict
        self.assertEqual(type(MyView1.base_mixins), SortedDict)

    def test_view_keep_mixins_ordered(self):
        self.assertEqual(MyView1.base_mixins.keys(), ['mixin1', 'mixin2'])
        self.assertEqual(MyView2.base_mixins.keys(), ['mixin2', 'mixin1'])

    def test_view_keep_mixins_ordered_when_subclassed(self):
        self.assertEqual(MySubView.base_mixins.keys(), ['mixin1', 'mixin2', 'mixin3'])

    def test_changing_the_instance_mixins_does_not_affect_the_class(self):
        view = MyView1(mode='detail')
        self.assertEqual(view.mixins.keys(), ['mixin1', 'mixin2'])
        from django.utils.datastructures import SortedDict
        view.mixins = SortedDict()
        self.assertEqual(view.mixins.keys(), [])
        self.assertEqual(MyView1.base_mixins.keys(), ['mixin1', 'mixin2'])

    def test_authorizations(self):
        from  django.core.exceptions import PermissionDenied
        view = ForbiddenView(mode='detail')
        rf = RequestFactory()
        request = rf.get('/')
        with self.assertRaises(PermissionDenied):
            view.dispatch(request)

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


#
# ObjectMixin tests
#

class MyObjectModel(models.Model):
    pass


class MyOtherObjectModel(models.Model):
    pass


class MyObjectMixin(ObjectMixin):
    model = MyObjectModel


class MyOtherObjectMixin(ObjectMixin):
    model = MyOtherObjectModel


class ObjectView(View):
    obj = MyObjectMixin()
    other = MyOtherObjectMixin(mode='list')


class TestObjectMixin(TestCase):

    def test_template_names(self):
        object_mixin = MyObjectMixin()
        object_mixin.mode = 'list'
        template_names = object_mixin.get_template_names()
        self.assertEqual(template_names, [
            'alternative_views/myobjectmodel_list.html'
        ])

        object_mixin.mode = 'detail'
        object_mixin.template_name_prefix = 'demo/project'
        template_names = object_mixin.get_template_names()
        self.assertEqual(template_names, [
            'demo/project_detail.html',
            'alternative_views/myobjectmodel_detail.html',
        ])


class TestObjectMixinIntegrationWithView(TestCase):

    def test_setting_mode_on_creation_does_not_override_class_value(self):
        view = ObjectView(mode='list')
        instance_mode = view.mixins['other'].mode
        self.assertEqual(instance_mode, 'list')

        view = ObjectView(mode='detail')
        instance_mode = view.mixins['other'].mode
        self.assertEqual(instance_mode, 'list')

    def test_same_mixins_with_different_names(self):
        self.assertTrue(False)

    def test_context_for_list_mode(self):
        view = ObjectView.as_view(mode='list')
        rf = RequestFactory()
        request = rf.get('/')
        response = view(request)
        self.assertEqual(response.context_data.keys(),
            ['myotherobjectmodel_list', 'myobjectmodel_list'])

    def test_context_for_detail_mode(self):
        view = ObjectView.as_view(mode='detail')
        rf = RequestFactory()
        request = rf.get('/')
        response = view(request)
        self.assertEqual(response.context_data.keys(),
            ['myotherobjectmodel_list', 'myobjectmodel'])
