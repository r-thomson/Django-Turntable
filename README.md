# Django-Turntable

This is a lightweight Django library that helps developers optimize their app's database access.

With Django’s ORM, it’s very easy to write code that executes a lot of redundant database queries, or to create queries that are very slow. This library can track all queries that are executed within a block of code, then:

* Tell you how many queries were executed
* Tell you how long those queries took to execute
* Warn you if the same query is executed repeatedly (the [“N+1 selects problem”](https://stackoverflow.com/q/97197))

Here’s an example of what the output looks like (with `logging.basicConfig()`):

```
INFO:django_turntable:12 queries executed (0.364ms)
WARNING:django_turntable:Repeating query (10x): SELECT "music_artist"."id", "music_artist"."name" FROM "music_artist" WHERE "music_artist"."id" = %s LIMIT 21
```

# Documentation

## Context Manager

Use `inspect_queries()` as a context manager to examine all query usage within the body of the `with` statement. A summary will be logged when exiting the block (even if an exception occurs).

```py
from django_turntable import inspect_queries

with inspect_queries():
    ...
```

## Decorator

`inspect_queries()` can also be used as a function decorator.

```py
from django_turntable import inspect_queries

@inspect_queries()
def some_function():
    ...
```

## Middleware

Use the `TurntableMiddleware` to monitor query usage in your views, as well as any middleware placed *below* `TurntableMiddleware`.

```py
MIDDLEWARE = [
    'django_turntable.TurntableMiddleware',
]
```

Because this library is intended as a development tool, the middleware will automatically remove itself if the [`DEBUG` setting](https://docs.djangoproject.com/en/dev/ref/settings/#std-setting-DEBUG) is set to `False`.

## Logging

All output is sent to the `django_turntable` logger. In your logging configuration, you should set this logger's level to `INFO` if you want to see all query usage, or `WARNING` if you just want to see potential problems.
