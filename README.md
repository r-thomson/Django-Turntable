# Django-Turntable

This is a lightweight Django library for helping developers optimize their app's database access.

**Currently**, this library just counts the number of queries executed.

**In the future**, it will analyze your SQL queries to identify repeating queries.

## Usage

### As a Context Manager

```py
from django_turntable import inspect_queries

with inspect_queries():
    ...
```

### As a Decorator

```py
from django_turntable import inspect_queries

@inspect_queries()
def my_function():
    ...
```

### As Middleware

```py
# settings.py

MIDDLEWARE = [
    ...,
    'django_turntable.TurntableMiddleware',
]
```
