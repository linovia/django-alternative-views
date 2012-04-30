from __future__ import absolute_import

from django.conf.urls import patterns, url

from alternative_views.base import View
from alternative_views.mixins.object import ObjectMixin

from ..models import MyObjectModel, MyOtherObjectModel


class MyObjectMixin(ObjectMixin):
    model = MyObjectModel


class MyOtherObjectMixin(ObjectMixin):
    model = MyOtherObjectModel


class ObjectView(View):
    other = MyOtherObjectMixin(mode='list')
    obj = MyObjectMixin()


class SameMixinView(View):
    obj1 = MyObjectMixin()
    obj2 = MyObjectMixin()


urlpatterns = patterns('',
    url(r'^object/$', ObjectView.as_view(mode='list'), name='object_list'),
    url(r'^object/new/$', ObjectView.as_view(mode='new'), name='object_new'),
    url(r'^object/(?P<pk>\d+)/$', ObjectView.as_view(mode='detail'), name='object_detail'),
    url(r'^object/(?P<pk>\d+)/update/$', ObjectView.as_view(mode='update'), name='object_update'),
    url(r'^object/(?P<pk>\d+)/delete/$', ObjectView.as_view(mode='delete'), name='object_delete'),
)
