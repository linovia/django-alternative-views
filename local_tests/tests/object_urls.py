from __future__ import absolute_import

from django.conf.urls import patterns
from django.core.urlresolvers import reverse

from alternative_views.base import View
from alternative_views.mixins.object import ObjectMixin

from ..models import MyObjectModel, MyOtherObjectModel


class MyObjectMixin(ObjectMixin):
    model = MyObjectModel

    def get_success_url(self):
        return '/object/3/'
        return reverse('detail', kwargs={'pk': self.object.id})


class MyOtherObjectMixin(ObjectMixin):
    model = MyOtherObjectModel


class ObjectView(View):
    other = MyOtherObjectMixin(mode='list')
    obj = MyObjectMixin()


class SameMixinView(View):
    obj1 = MyObjectMixin()
    obj2 = MyObjectMixin()


urlpatterns = patterns('',
    (r'^object/$', ObjectView.as_view(mode='list')),
    (r'^object/new/$', ObjectView.as_view(mode='new')),
    (r'^object/(?P<pk>\d+)/$', ObjectView.as_view(mode='detail')),
    (r'^object/(?P<pk>\d+)/update/$', ObjectView.as_view(mode='update')),
    (r'^object/(?P<pk>\d+)/delete/$', ObjectView.as_view(mode='delete')),
)
