from functools import wraps
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator


def exclude_roles(*excluded_roles: object):
    def decorator(func_or_class):
        if isinstance(func_or_class, type):
            original_dispatch = func_or_class.dispatch

            @method_decorator(exclude_roles(*excluded_roles))
            def new_dispatch(self, request, *args, **kwargs):
                return original_dispatch(self, request, *args, **kwargs)

            func_or_class.dispatch = new_dispatch
            return func_or_class

        @wraps(func_or_class)
        def wrapped_view(request,*args,**kwargs):
            if request.user.role.work_title in excluded_roles:
                return redirect('access-denied')
            return func_or_class(request,*args,**kwargs)
        return wrapped_view
    return decorator


def allow_roles(*allowed_roles: object):
    def decorator(func_or_class):
        if isinstance(func_or_class, type):
            original_dispatch = func_or_class.dispatch

            @method_decorator(exclude_roles(*allowed_roles))
            def new_dispatch(self, request, *args, **kwargs):
                return original_dispatch(self, request, *args, **kwargs)

            func_or_class.dispatch = new_dispatch
            return func_or_class

        @wraps(func_or_class)
        def wrapped_view(request, *args, **kwargs):
            if request.user.role.work_title not in allowed_roles:
                return redirect('access-denied')
            return func_or_class(request, *args, **kwargs)

        return wrapped_view

    return decorator