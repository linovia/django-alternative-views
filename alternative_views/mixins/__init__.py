

class Mixin(object):

    # Tracks each time a Field instance is created. Used to retain order.
    creation_counter = 0

    # ['get', 'post', 'put', 'delete', 'head', 'options', 'trace']
    allowed_methods = []

    def __init__(self, *args, **kwargs):
        self.type = None
        super(Mixin, self).__init__(*args, **kwargs)

        # Increase the creation counter, and save our local copy.
        self.creation_counter = Mixin.creation_counter
        Mixin.creation_counter += 1

    def contribute_to_view(self, request):
        """
        Returns a dictionary that will be "merged" in the following Mixins.
        """
        return {}

    def can_handle_method(self, name, mode):
        """
        Return whether this mixin can handle a given http method.
        """
        if hasattr(self, '%s_%s' % (mode, name)):
            return True
        if hasattr(self, name):
            return True
        return False

    def get_template_names(self):
        return []
