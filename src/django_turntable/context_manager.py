import logging
from collections.abc import Callable
from contextlib import contextmanager
from typing import Any

import django.db
from django.db.backends.base.base import BaseDatabaseWrapper

logger = logging.getLogger('django_turntable')


@contextmanager
def inspect_queries(connection: BaseDatabaseWrapper | None = None):
    if connection is None:
        connection = django.db.connection

    n = 0

    def wrapper(
        execute: Callable[[str, Any, bool, dict[str, Any]], Any],
        sql: str,
        params: Any,
        many: bool,
        context: dict[str, Any],
    ) -> Any:
        nonlocal n
        n += 1

        return execute(sql, params, many, context)

    try:
        with connection.execute_wrapper(wrapper):
            yield
    finally:
        if n:
            logger.info(f'{n} queries executed')
