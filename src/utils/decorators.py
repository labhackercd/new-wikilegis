from django.core.exceptions import PermissionDenied


def require_ajax(function):
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            raise PermissionDenied()
        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
