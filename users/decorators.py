from django.http import HttpResponseForbidden
from functools import wraps

def client_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:  # Allow superuser access
            return view_func(request, *args, **kwargs)
        if request.user.role == 'Client':  # Match title case
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You are not authorized to view this page.")
    return _wrapped_view



def freelancer_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:  # Allow superuser access
            return view_func(request, *args, **kwargs)
        if request.user.role == 'Freelancer':  # Match title case
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You are not authorized to view this page.")
    return _wrapped_view
