SECRET_KEY = 'fake-key'


INSTALLED_APPS = [
    "tests",
]


ROOT_URLCONF = 'tests.urls'


WSGI_APPLICATION = 'test.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    }
}


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
)
