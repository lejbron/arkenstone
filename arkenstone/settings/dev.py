from .base import *  # noqa

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),  # noqa
        'USER': config('DB_USER'),  # noqa
        'PASSWORD': config('DB_PASSWORD'),  # noqa
        'HOST': config('DB_HOST'),  # noqa
        'PORT': '',
    }
}

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),  # noqa
)
