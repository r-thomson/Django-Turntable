# Django-Turntable

This is a lightweight Django library for helping developers optimize their app's database access.

**Currently**, this library just counts the number of queries executed.

**In the future**, it will analyze your SQL queries to identify repeating queries.

# Documentation

## Context Manager

```py
from django_turntable import inspect_queries

with inspect_queries():
    ...
```

## Decorator

Works identically to the context manager.

```py
from django_turntable import inspect_queries

@inspect_queries()
def my_function():
    ...
```

## Middleware

Any middleware placed *below* `TurntableMiddleware` will have its query usage monitored as well.

```py
MIDDLEWARE = [
    # ...
    'django_turntable.TurntableMiddleware',
    # ...
]
```

Because this library is intended as a development tool, the middleware will automatically remove itself if the `DEBUG` setting is set to `False`.

## Logging

All output is sent to the `django_turntable` logger. In your logging configuration, you should set this logger's level to `INFO` if you want to see all query usage, or `WARNING` if you just want to see potential problems.
