from __future__ import absolute_import

from django.conf.urls import patterns, url
from django.views.decorators.cache import cache_page
# from django.views.generic import TemplateView

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


urlpatterns = patterns('',
    (r'^object/(?P<pk>\d+)/$', ObjectView.as_view(mode='detail')),
)
