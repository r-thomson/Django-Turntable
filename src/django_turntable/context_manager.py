import logging
from collections import Counter, deque
from collections.abc import Callable
from contextlib import contextmanager
from dataclasses import dataclass
from math import fsum
from timeit import default_timer as timer
from typing import Any

import django.db
from django.db.backends.base.base import BaseDatabaseWrapper

logger = logging.getLogger('django_turntable')


@dataclass(frozen=True, slots=True)
class QueryRecord:
    sql: str
    time: float


@contextmanager
def inspect_queries(connection: BaseDatabaseWrapper | None = None):
    if connection is None:
        connection = django.db.connection

    queries = deque[QueryRecord]()

    def wrapper(
        execute: Callable[[str, Any, bool, dict[str, Any]], Any],
        sql: str,
        params: Any,
        many: bool,
        context: dict[str, Any],
    ) -> Any:
        start = timer()

        try:
            return execute(sql, params, many, context)
        finally:
            end = timer()
            queries.append(QueryRecord(sql, time=(end - start)))

    try:
        with connection.execute_wrapper(wrapper):
            yield
    finally:
        n = len(queries)
        t = fsum(q.time for q in queries)

        if n:
            logger.info(f'{n} queries executed ({t * 1000:.3f}ms)')

        counter = Counter(q.sql for q in queries)
        for sql, count in counter.items():
            if count > 3:
                logger.warning(f'Repeating query ({count}x): {sql}')


__all__ = ['inspect_queries']
