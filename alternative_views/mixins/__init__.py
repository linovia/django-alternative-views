
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ImproperlyConfigured
from django.template.response import TemplateResponse


class BaseMixin(object):

    # Tracks each time a Field instance is created. Used to retain order.
    creation_counter = 0

    def __init__(self, *args, **kwargs):
        self.type = None
        super(BaseMixin, self).__init__(*args, **kwargs)

        # Increase the creation counter, and save our local copy.
        self.creation_counter = Mixin.creation_counter
        Mixin.creation_counter += 1


class Mixin(BaseMixin):
    mode = None
    template_name = None
    response_class = TemplateResponse

    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options', 'trace']

    def authorization(self, request, context):
        """
        Returns True if the user has enough rights for this request.
        """
        return True

    def get_context(self, request, context):
        """
        Returns an updated context for the given request processing.
        """
        if not self.authorization(request, context):
            raise PermissionDenied()
        return context

    def can_process(self, request):
        """
        Return True if that mixin can handle the given method.
        """
        return request.method.lower() in self.http_method_names

    def process(self, request, context):
        """
        Process the request
        """
        return self.render_to_response(request, context)

    def render_to_response(self, request, context, **response_kwargs):
        """
        Returns a response with a template rendered with the given context.
        """
        return self.response_class(
            request=request,
            template=self.get_template_names(),
            context=context,
            **response_kwargs
        )

    def get_template_names(self):
        """
        Returns a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response is overridden.
        """
        if self.template_name is None:
            raise ImproperlyConfigured(
                "%s requires either a definition of 'template_name' "
                "or an implementation of 'get_template_names()'" % (type(self))
            )
        else:
            return [self.template_name]
