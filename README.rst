Django alternative views
========================

.. image:: https://secure.travis-ci.org/linovia/django-alternative-views.png?branch=master
   :alt: Build Status
   :target: http://travis-ci.org/linovia/django-alternative-views

This is work in progress and shouldn't be used yet.

This package provides an alternative implementation of Django generic
class based views.

It is aimed to be much more reusable and should cover a wider set of use
cases.


Target
------

views.py::


    class ProjectMixin(ObjectMixin):
        model = Project
        pk_url_kwarg = 'project_id'
    

    class ContactMixin(FormMixin):
        form = ContactForm


    class BugMixin(ObjectMixin):
        model = Bug
        pk_url_kwarg = 'bug_id'

        def get_queryset(self):
            # Limits the bugs to the current project's ones
            return Bug.objects.filter(self.project)


    class ProjectView(View):
        contact = ContactMixin()
        project = ProjectMixin()


    class BugView(ProjectView):
        # Automatically inherit mixins from ProjectView
        bug = BugMixin()


    
urls.py::


    urlpatterns = patterns('',
        url(r'^project/$', ProjectView.as_view('list'), name='projects'),
        url(r'^project/new/$', ProjectView.as_view('new'), name='new-project'),
        url(r'^project/(?P<project_id>\d+)/$', ProjectView.as_view('detail'), name='project'),
        url(r'^project/(?P<project_id>\d+)/update/$', ProjectView.as_view('update'), name='update-project'),
        url(r'^project/(?P<project_id>\d+)/delete/$', ProjectView.as_view('delete'), name='delete-project'),

        url(r'^project/(?P<project_id>\d+)/bugs/$', BugView.as_view('list'), name='project-bugs'),
        url(r'^project/(?P<project_id>\d+)/bugs/new/$', BugView.as_view('new'), name='new-project-bug'),
        url(r'^project/(?P<project_id>\d+)/bugs/(?P<bug_id>\d+)/$', BugView.as_view('detail'), name='project-bug'),
        url(r'^project/(?P<project_id>\d+)/bugs/(?P<bug_id>\d+)/update/$', BugView.as_view('update'), name='update-project-bug'),
        url(r'^project/(?P<project_id>\d+)/bugs/(?P<bug_id>\d+)/delete/$', BugView.as_view('delete'), name='delete-project-bug'),
    )

