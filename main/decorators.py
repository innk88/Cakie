# myapp/decorators.py
from functools import wraps
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

User = get_user_model()


def check_user_permission(permission):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            user = User.objects.get(pk=request.user.pk)  # Извлекаем реальный объект пользователя
            if not user.has_perm(permission):
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
