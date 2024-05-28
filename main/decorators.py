# myapp/decorators.py
from functools import wraps
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from .models import Person, Chief

User = get_user_model()


def check_user_permission(permission):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            user = User.objects.get(pk=request.user.pk)
            if not user.has_perm(permission):
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def get_real_user(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        if isinstance(request.user, Person):
            request.real_user = request.user
        else:
            try:
                real_user = Person.objects.get(pk=request.user.pk)
                request.real_user = real_user
            except Person.DoesNotExist:
                raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def check_if_chief(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if isinstance(request.user, Chief):
            request.is_chief = True
        else:
            try:
                Chief.objects.get(pk=request.user.pk)
                request.is_chief = True
            except Chief.DoesNotExist:
                request.is_chief = False
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def get_real_chief(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        if isinstance(request.user, Chief):
            request.real_chief = request.user
        else:
            try:
                real_chief = Chief.objects.get(pk=request.user.pk)
                request.real_chief = real_chief
            except Chief.DoesNotExist:
                raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view