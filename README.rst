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
    

    class SomeView(View):
        project = ProjectMixin()
        contact = ContactMixin()

    
urls.py::


    urlpatterns = patterns('',
        url(r'^project/$', ProjectView.as_list(), name='projects'),
        url(r'^project/new/$', ProjectView.as_new(), name='new-project'),
        url(r'^project/(?P<project_id>\d+)/$', ProjectView.as_detail(), name='project'),
        url(r'^project/(?P<project_id>\d+)/update/$', ProjectView.as_update(), name='update-project'),
        url(r'^project/(?P<project_id>\d+)/delete/$', ProjectView.as_delete(), name='delete-project'),
    )

