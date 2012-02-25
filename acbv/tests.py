
# from django.test import TestCase
from django.test import RequestFactory
from unittest2 import TestCase
from base import View, Mixin
from mock import Mock
import types
import copy


class MyMixin1(Mixin):
    pass


class MyMixin2(Mixin):
    pass


class MyView1(View):
    mixin1 = MyMixin1()
    mixin2 = MyMixin2()


class MyView2(View):
    mixin2 = MyMixin2()
    mixin1 = MyMixin1()


class MySubView(MyView1):
    mixin3 = MyMixin1()


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
        view = MyView1()
        self.assertEqual(view.mixins.keys(), ['mixin1', 'mixin2'])
        from django.utils.datastructures import SortedDict
        view.mixins = SortedDict()
        self.assertEqual(view.mixins.keys(), [])
        self.assertEqual(MyView1.base_mixins.keys(), ['mixin1', 'mixin2'])

    def test_mixins_contribute_to_view_is_called_from_view(self):
        view = MyView1()
        m1, m2 = Mock(), Mock()
        m1.return_value, m2.return_value = {}, {}
        view.mixins['mixin1'].contribute_to_view = m1
        view.mixins['mixin2'].contribute_to_view = m2
        request = Mock()
        view.contribute_to_view(request)
        self.assertTrue(m1.called)
        self.assertEqual(m1.call_count, 1)
        self.assertTrue(m2.called)
        self.assertEqual(m2.call_count, 1)

    def test_mixin_can_access_other_mixin_context(self):
        view = MyView1()
        test_data = {
            'mixin1_variable': 34,
            'demo_info': 'azerty',
        }
        test_case = self

        def contribute_to_view1(self, request):
            return copy.deepcopy(test_data)

        def contribute_to_view2(self, request):
            for key, value in test_data.iteritems():
                test_case.assertTrue(hasattr(self, key))
                test_case.assertEqual(getattr(self, key), value)
            return {}

        mixin1, mixin2 = view.mixins['mixin1'], view.mixins['mixin2']
        mixin1.contribute_to_view = types.MethodType(contribute_to_view1, mixin1)
        mixin2.contribute_to_view = types.MethodType(contribute_to_view2, mixin2)
        request = Mock()
        view.contribute_to_view(request)

    def test_method_not_allowed_if_no_mixins_can_process_it(self):
        view = MyView1()
        rf = RequestFactory()
        request = rf.get('/')
        view.dispatch(request)
        raise NotImplementedError('')
