import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-s$io6_xls$2hgu)%n(8w8&4pfiw0-vzju-ow!^b(2h2*wc!m3i"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "unfold",
    "ckeditor",
    "ckeditor_uploader",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_multiple_model",
    "tinymce",
    "home",
    "about",
    "activity",
    "blog",
    "guide",
    "django_summernote",
    "solo",
    "corsheaders",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "hikingbees.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [Path(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "hikingbees.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

""" DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
} """

DATA_UPLOAD_MAX_MEMORY_SIZE = None
""" DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "hikingbees",
        "USER": "vishal",
        "PASSWORD": "DatabaseUserPassword",
        "HOST": "localhost",
        "PORT": "",
    }
} """

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "HZJDQRX5WI0YMu0ZIcxXYOszI4bUKmUsfyBjaliAojBWzQ4NiQ9tvmFjLUF2OR9B",
        "HOST": "agsks8c0owoswc0cg8wwkosc",
        "PORT": "5432",
    }
}
# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = "/static/"
STATICFILES_DIRS = []
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

CKEDITOR_UPLOAD_PATH = "uploads/"

MEDIA_URL = "/media/"
MEDIA_ROOT = Path(BASE_DIR, "media")
CORS_ALLOW_ALL_ORIGINS = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

X_FRAME_OPTIONS = "SAMEORIGIN"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.zoho.com"
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_PORT = 465
EMAIL_HOST_USER = "info@hikingbees.com"
EMAIL_HOST_PASSWORD = "20@Hikingbees20."


SUMMERNOTE_CONFIG = {
    "summernote": {
        "width": "100%",
        "toolbar": [
            [
                "style",
                [
                    "style",
                ],
            ],
            [
                "font",
                [
                    "fontname",
                    "fontsize",
                    "bold",
                    "italic",
                    "strikethrough",
                    "clear",
                ],
            ],
            [
                "color",
                [
                    "forecolor",
                    "backcolor",
                ],
            ],
            ["para", ["ul", "ol", "height"]],
            ["insert", ["link"]],
            [
                "misc",
                [
                    "picture",
                    "fullscreen",
                    "codeview",
                    "print",
                    "help",
                ],
            ],
        ],
        "fontNames": ["Roboto"],
    }
}
SUMMERNOTE_THEME = "bs4"

TINYMCE_DEFAULT_CONFIG = {
    "height": "780",
    "width": "780",
    "entity_encoding": "raw",
    "menubar": "file edit view insert format tools table help",
    "plugins": "print preview paste importcss searchreplace autolink autosave save code visualblocks visualchars fullscreen image link media template codesample table charmap hr pagebreak nonbreaking anchor toc insertdatetime advlist lists wordcount imagetools textpattern noneditable help charmap emoticons quickbars",
    "toolbar": "fullscreen preview | undo redo | bold italic forecolor backcolor | formatselect | image link | "
    "alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | fontsizeselect "
    "emoticons | ",
    "custom_undo_redo_levels": 50,
    "quickbars_insert_toolbar": False,
    "file_picker_callback": """function (cb, value, meta) {
        var input = document.createElement("input");
        input.setAttribute("type", "file");
        if (meta.filetype == "image") {
            input.setAttribute("accept", "image/*");
        }
        if (meta.filetype == "media") {
            input.setAttribute("accept", "video/*");
        }

        input.onchange = function () {
            var file = this.files[0];
            var reader = new FileReader();
            reader.onload = function () {
                var id = "blobid" + (new Date()).getTime();
                var blobCache = tinymce.activeEditor.editorUpload.blobCache;
                var base64 = reader.result.split(",")[1];
                var blobInfo = blobCache.create(id, file, base64);
                blobCache.add(blobInfo);
                cb(blobInfo.blobUri(), { title: file.name });
            };
            reader.readAsDataURL(file);
        };
        input.click();
    }""",
    "content_style": "body { font-family:Roboto,Helvetica,Arial,sans-serif; font-size:14px }",
}

CSRF_TRUSTED_ORIGINS = [
    "https://4963-110-44-120-22.ngrok.io",
]


UNFOLD = {
    "SITE_HEADER": _("Hikingbees Admin"),
    "SITE_TITLE": _("Hikingbees Admin"),
    "SITE_BRAND": _("Hikingbees"),
    "THEME": "",
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation_expanded": True,
    },
    "WELCOME_MESSAGE": _("Welcome to the Hikingbees Admin"),
    "COPYRIGHT": _("Baliyo Software"),
    "SEARCH_MODELS": ["blog.post", "activity.activity"],
    "SHOW_UI_BUILDER": False,
    "HIDE_APPS": ["auth"],
    "ORDER_WITH_RESPECT_TO": ["home", "activity", "blog"],
}
