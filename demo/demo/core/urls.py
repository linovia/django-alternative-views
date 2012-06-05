from django.conf.urls import patterns, include, url

from demo.core.views import ProjectView, BugView


bug_urlpatterns = patterns('',
    url(r'^$',
        BugView.as_view(mode='list'),
        name='bugs'),
    url(r'^new/$',
        BugView.as_view(mode='new'),
        name='new-bug'),
)


urlpatterns = patterns('',
    url(r'^projects/$',
        ProjectView.as_view(mode='list'),
        name='projects'),
    url(r'^projects/new/$',
        ProjectView.as_view(mode='new'),
        name='new-project'),
    url(r'^projects/(?P<project_id>\d+)/$',
        ProjectView.as_view(mode='detail'),
        name='project'),
    url(r'^projects/(?P<project_id>\d+)/update/$',
        ProjectView.as_view(mode='update'),
        name='update-project'),
    url(r'^projects/(?P<project_id>\d+)/delete/$',
        ProjectView.as_view(mode='delete'),
        name='delete-project'),

    (r'^projects/(?P<project_id>\d+)/bugs/',    include(bug_urlpatterns)),
)
