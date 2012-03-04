Django alternative views
========================

This is work in progress and shouldn't be used yet.

This package provides an alternative implementation of Django generic
class based views.

It is aimed to be much more reusable and should cover a wider set of use
cases.


Examples
--------

::


    class ProjectMixin(ObjectMixin):
        model = Project
        pk_url_kwarg = 'project_id'
    

    class ContactMixin(FormMixin):
        form = ContactForm
    

    class SomeView(View):
        project = ProjectMixin()
        contact = ContactMixin()

    