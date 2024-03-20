import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

load_dotenv()


def load_bool(name, default):
    env_value = os.getenv(name, str(default)).lower()
    return env_value in {"true", "yes", "1", "y", "t"}


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "test")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = load_bool("DJANGO_DEBUG", True)

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(",")

ALLOW_REVERSE = load_bool("DJANGO_ALLOW_REVERSE", True)

DJANGO_MAIL = os.getenv("DJANGO_MAIL", "aboba@main.ru")
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "sorl.thumbnail",
    "tinymce",
    "about.apps.AboutConfig",
    "catalog.apps.CatalogConfig",
    "download.apps.DownloadConfig",
    "feedback.apps.FeedbackConfig",
    "homepage.apps.HomepageConfig",
    "django_cleanup.apps.CleanupConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "lyceum.middleware.ReverseMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
    INTERNAL_IPS = ["127.0.0.1", "localhost"]

ROOT_URLCONF = "lyceum.urls"

TEMPLATES_DIRS = BASE_DIR / "templates"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIRS],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "lyceum.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation"
        ".UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".NumericPasswordValidator",
    },
]

LANGUAGES = [
    ("en", _("English")),
    ("ru", _("Русский")),
]

LOCALE_PATHS = (BASE_DIR / "locale",)

LANGUAGE_CODE = "ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"

STATICFILES_DIRS = [BASE_DIR / "static_dev/"]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "send_mail"

__all__ = []
