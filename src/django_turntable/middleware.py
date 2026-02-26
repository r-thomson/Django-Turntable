from collections.abc import Callable

from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.http import HttpRequest, HttpResponse

from .context_manager import inspect_queries


class TurntableMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        if not settings.DEBUG:
            raise MiddlewareNotUsed

        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        with inspect_queries():
            return self.get_response(request)


__all__ = ['TurntableMiddleware']
