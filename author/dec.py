from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
import functools


def login_denied(fn):
    @functools.wraps(fn)
    def wrapper(request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('home'))
        return fn(request)

    return wrapper
