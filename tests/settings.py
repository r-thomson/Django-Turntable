SECRET_KEY = 'test_secret_key'

DEBUG = True

INSTALLED_APPS = [
    'tests',
]

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django_turntable.TurntableMiddleware',
]

ROOT_URLCONF = 'tests.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

USE_TZ = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {'format': '%(levelname)s:%(name)s:%(message)s'},
    },
    'handlers': {
        'default': {'class': 'logging.StreamHandler', 'formatter': 'default'},
    },
    'loggers': {
        'django_turntable': {'level': 'INFO', 'handlers': ['default']},
    },
}
