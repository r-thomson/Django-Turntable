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
