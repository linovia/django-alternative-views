
from django.conf.urls import patterns, url
from core import views

urlpatterns = patterns('',
    url(r'^$', views.ProjectView.as_view(mode='list')),
)
