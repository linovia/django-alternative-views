"""

"""

from alternative_views.mixins import Mixin
from alternative_views.base import View

from django.test import TestCase


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
        self.assertEqual(
            MySubView.base_mixins.keys(),
            ['mixin1', 'mixin2', 'mixin3']
        )

    def test_changing_the_instance_mixins_does_not_affect_the_class(self):
        view = MyView1(mode='detail')
        self.assertEqual(view.mixins.keys(), ['mixin1', 'mixin2'])
        from django.utils.datastructures import SortedDict
        view.mixins = SortedDict()
        self.assertEqual(view.mixins.keys(), [])
        self.assertEqual(MyView1.base_mixins.keys(), ['mixin1', 'mixin2'])
