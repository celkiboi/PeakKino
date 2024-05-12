from functools import wraps
from django.http import HttpResponseForbidden

def staff_required(view_function):
    @wraps(view_function)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden('Only staff can view this content')
        return view_function(request, *args, **kwargs)
    return wrapper