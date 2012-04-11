Design thoughts
~~~~~~~~~~~~~~~

This document are my rants about what I'd like to see as generic views.
It will explains the choices made in the design.


WHat should the user code looks like ?
======================================

views.py::


    class ProjectMixin(ModelMixin):
        model = Project
        pk_url_kwarg = 'project_id'

        def get_queryset(self):
            user = self.request.user
            return user.projects.all()
    

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



ModelMixin
==========

They should be able to "morph" according to how the view is called.
For example if ProjectView.as_update is called, then the ModelMixin should
be able to adapt into an UpdateView.

Issue: The mixin is instanciated by the time the View is declared while it
should be specialized when the as_* is called.

Proposed solution:
Do something similar to forms and BoundFields. Using that sort of trick
could allow to defer specialisation when it is needed.
Possibly, Django Class Based Views could be reused here.


Forseen issues
==============

* Use prefix in forms so that we can make sure which form has been posted if
several are available.

* Reverse order: Mixins' get or post should be processed from bottom to top.
The most specialised mixin in the view should be the lastest while the most
general one should be on top.



Required for Mixins
===================

* Context generation: function that should take a context dict as argument and
return the updated context. The returned context will be passed to the following
mixins so that one mixin that depends on the other will still be able to
specialize its data.

* Authorization: Probably called by the context generation function.

* Request method check: should respond True or False according to the ability
to answer a given request type.

* Template name: returns a template name. The view should probably call this
function in the reverse mixin order.
