from functools import wraps
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def role_required(role):
    """
    Decorator that checks `request.user.role == role`.
    `role` can be a single role string or an iterable of roles.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')  # or your login url name
            roles = role if isinstance(role, (list, tuple, set)) else (role,)
            if request.user.role not in roles and not request.user.is_superuser:
                raise PermissionDenied("You don't have permission to access this view.")
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator
