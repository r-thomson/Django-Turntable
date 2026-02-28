import logging
from collections.abc import Callable
from contextlib import contextmanager
from timeit import default_timer as timer
from typing import Any

import django.db
from django.db.backends.base.base import BaseDatabaseWrapper

logger = logging.getLogger('django_turntable')


@contextmanager
def inspect_queries(connection: BaseDatabaseWrapper | None = None):
    if connection is None:
        connection = django.db.connection

    n = 0
    t = 0.0

    def wrapper(
        execute: Callable[[str, Any, bool, dict[str, Any]], Any],
        sql: str,
        params: Any,
        many: bool,
        context: dict[str, Any],
    ) -> Any:
        nonlocal n, t

        n += 1
        start = timer()

        try:
            return execute(sql, params, many, context)
        finally:
            end = timer()
            t += end - start

    try:
        with connection.execute_wrapper(wrapper):
            yield
    finally:
        if n:
            logger.info(f'{n} queries executed ({t * 1000:.3f}ms)')


__all__ = ['inspect_queries']
