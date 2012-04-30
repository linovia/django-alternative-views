"""

"""

from django.test import RequestFactory

from django.test import TestCase

from alternative_views.base import View
from alternative_views.mixins.object import ObjectMixin

from ..models import MyObjectModel, MyOtherObjectModel


class MyObjectMixin(ObjectMixin):
    model = MyObjectModel


class MyOtherObjectMixin(ObjectMixin):
    model = MyOtherObjectModel


class ObjectView(View):
    obj = MyObjectMixin()
    other = MyOtherObjectMixin(mode='list')


class SameMixinView(View):
    obj1 = MyObjectMixin()
    obj2 = MyObjectMixin()


class TestObjectMixin(TestCase):

    def test_template_names(self):
        object_mixin = MyObjectMixin(mode='list')
        object_mixin.instance_name = 'myobjectmodel'
        template_names = object_mixin.get_template_names()
        self.assertEqual(template_names, [
            'local_tests/myobjectmodel_list.html'
        ])

        object_mixin.mode = 'detail'
        object_mixin.template_name_prefix = 'demo/project'
        template_names = object_mixin.get_template_names()
        self.assertEqual(template_names, [
            'demo/project_detail.html',
            'local_tests/myobjectmodel_detail.html',
        ])

    def test_as_mode(self):
        mixin = MyObjectMixin()
        mixin.as_mode('list')
        from alternative_views.mixins.object import AlternativeMultipleObjectMixin
        self.assertTrue(isinstance(mixin, MyObjectMixin))
        self.assertTrue(isinstance(mixin, AlternativeMultipleObjectMixin))


class TestObjectListMixin(TestCase):

    def test_context(self):
        mixin = MyObjectMixin()
        mixin.instance_name = 'mixin_object'
        mixin.as_mode('list')
        rf = RequestFactory()
        request = rf.get('/')
        context = mixin.get_context(request, {})
        # QuerySet -> List to try to compare in the assert.
        context['mixin_object_list'] = list(context['mixin_object_list'])
        expected = {
            'is_paginated': False,
            'mixin_object_list': list(MyObjectModel.objects.all()),
            'page_obj': None,
            'paginator': None,
        }
        self.assertEqual(expected, context)


class TestObjectMixinIntegrationWithView(TestCase):

    fixtures = ['basic_mixins_test.json']
    urls = 'local_tests.tests.object_urls'

    def test_setting_mode_on_creation_does_not_override_class_value(self):
        view = ObjectView(mode='list')
        self.assertEqual(view.mixins['obj'].mode, 'list')
        self.assertEqual(view.mixins['other'].mode, 'list')

        view = ObjectView(mode='detail')
        self.assertEqual(view.mixins['obj'].mode, 'detail')
        self.assertEqual(view.mixins['other'].mode, 'list')

    def test_same_mixins_with_different_names(self):
        view = SameMixinView.as_view(mode='list')
        rf = RequestFactory()
        request = rf.get('/')
        response = view(request)
        self.assertEqual(
            sorted(response.context_data.keys()),
            sorted(['paginator', 'page_obj', 'is_paginated', 'obj1_list', 'obj2_list']))

    def test_context_for_list_mode(self):
        response = self.client.get('/object/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response=response,
            template_name='local_tests/obj_list.html')
        self.assertEqual(
            sorted(response.context_data.keys()),
            sorted(['paginator', 'page_obj', 'is_paginated', 'obj_list', 'other_list']))
        self.assertEqual(
            [(o.id, type(o)) for o in response.context_data['obj_list']],
            [(o.id, type(o)) for o in MyObjectModel.objects.all()]
        )
        self.assertEqual(
            [(o.id, type(o)) for o in response.context_data['other_list']],
            [(o.id, type(o)) for o in MyOtherObjectModel.objects.all()]
        )

    def test_context_for_detail_mode(self):
        response = self.client.get('/object/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response=response,
            template_name='local_tests/obj_detail.html')
        self.assertEqual(
            sorted(response.context_data.keys()),
            sorted(['paginator', 'page_obj', 'is_paginated', 'obj', 'other_list']))
        self.assertEqual(
            response.context_data['obj'],
            MyObjectModel.objects.get(id=1)
        )
        self.assertEqual(
            [(o.id, type(o)) for o in response.context_data['other_list']],
            [(o.id, type(o)) for o in MyOtherObjectModel.objects.all()]
        )

    def test_context_for_new_mode(self):
        response = self.client.get('/object/new/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response=response,
            template_name='local_tests/obj_new.html')
        self.assertTrue('obj_form' in response.context_data)
        self.assertTrue(response.context_data['obj_form'])

    def test_object_creation(self):
        response = self.client.post('/object/new/', {
            'slug': 'demo',
        })
        self.assertEqual(response.status_code, 302)
