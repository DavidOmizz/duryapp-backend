
# Django settings for dury_app project.

# Generated by 'django-admin startproject' using Django 5.1.4.

# For more information on this file, see
# https://docs.djangoproject.com/en/5.1/topics/settings/

# For the full list of settings and their values, see
# https://docs.djangoproject.com/en/5.1/ref/settings/

from pathlib import Path
import os # Make sure this is imported

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3c(wb^vj@q8t3rikk)3a!i^w-ggm%oo(2-f#hyykpyo^gb)94i'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'app.apps.AppConfig',
    'storages', # Still useful, many storage backends inherit from it
    'django_bunny_storage', # Your Bunny.net storage backend
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware", # Add this line
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dury_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dury_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# If you plan to use PostgreSQL in production, uncomment and configure this:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'duryapp',
#         'USER': 'postgres',
#         'PASSWORD': '132001',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' # Good practice for collectstatic in production
# Set default storage for media files to BunnyStorage
DEFAULT_FILE_STORAGE = 'django_bunny_storage.storage.BunnyStorage'



# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}

# --- Cloudinary settings removed as you're switching to Bunny.net ---
# CLOUDINARY_STORAGE = {
#     'CLOUD_NAME': 'dhg8mqa6o',
#     'API_KEY': '339523357929551',
#     'API_SECRET': 'u5QlhL0CjtESQWKyyAjk3a6ZwRU',
# }
# DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage' # This line will be replaced by Bunny.net


CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",    # React development server
    "https://your-production-domain.com",    # Your production frontend URL
]
CORS_ALLOW_ALL_ORIGINS = True # Be careful with this in production. Only use specific origins.


CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]


CORS_ALLOW_HEADERS = [
    "content-type",
    "authorization",
    "x-csrftoken",
    "x-requested-with",
]

LOGIN_REDIRECT_URL = 'dashboard'

# -----------------------------------------------------------------
# Bunny.net Storage Configuration
# IMPORTANT: For production, use environment variables for BUNNY_USERNAME and BUNNY_PASSWORD.
# Never hardcode sensitive credentials in production!
BUNNY_USERNAME = os.environ.get('BUNNY_USERNAME', 'duryapp') # Replace 'duryapp-videos' with your actual Storage Zone Name
BUNNY_PASSWORD = os.environ.get('BUNNY_PASSWORD', '1d0a60bf-cf38-461d-bbc2ec88d33a-64bc-43cc') # Replace with your actual Storage Zone Password (API Key)
BUNNY_REGION = os.environ.get('BUNNY_REGION', 'jh') # Replace 'jh' with your actual Storage Zone Region Code (e.g., 'de', 'ny', 'sg', 'jh')
BUNNY_PULL_ZONE_URL = os.environ.get('BUNNY_PULL_ZONE_URL', 'https://durycdn.b-cdn.net/') # Replace with your actual CDN Pull Zone Hostname (e.g., https://yourpullzonename.b-cdn.net/)


import sys
import os

# --- START DEBUGGING BLOCK FOR BUNNYSTORAGE ---
try:
    from django_bunny_storage.storage import BunnyStorage as LoadedBunnyStorage
    print(f"DEBUG_SETTINGS: Successfully imported BunnyStorage from {LoadedBunnyStorage.__module__}.", file=sys.stderr)

    # Attempt to instantiate it with your settings
    _test_bunny_instance = None
    try:
        _test_bunny_instance = LoadedBunnyStorage(
            username=BUNNY_USERNAME,
            password=BUNNY_PASSWORD,
            region=BUNNY_REGION,
            pull_zone_url=BUNNY_PULL_ZONE_URL
        )
        print(f"DEBUG_SETTINGS: BunnyStorage instantiated successfully.", file=sys.stderr)
        if hasattr(_test_bunny_instance, 'url'):
            print(f"DEBUG_SETTINGS: BunnyStorage instance HAS 'url' method.", file=sys.stderr)
        else:
            print(f"DEBUG_SETTINGS: BunnyStorage instance DOES NOT HAVE 'url' method. (CRITICAL!)", file=sys.stderr)
            print(f"DEBUG_SETTINGS: Type of instance: {type(_test_bunny_instance)}", file=sys.stderr)
            print(f"DEBUG_SETTINGS: Dir of instance: {dir(_test_bunny_instance)}", file=sys.stderr) # List all methods/attributes
            
    except Exception as e:
        print(f"DEBUG_SETTINGS: ERROR during BunnyStorage instantiation: {e}", file=sys.stderr)
        print(f"DEBUG_SETTINGS: Please double-check your BUNNY_USERNAME, BUNNY_PASSWORD, BUNNY_REGION, BUNNY_PULL_ZONE_URL values or environment variables.", file=sys.stderr)
        print(f"DEBUG_SETTINGS: This error during instantiation might cause Django to fall back to a generic Storage.", file=sys.stderr)

except ImportError as e:
    print(f"DEBUG_SETTINGS: ImportError for django_bunny_storage.storage: {e}", file=sys.stderr)
    print(f"DEBUG_SETTINGS: Please ensure 'django-bunny-storage' is correctly installed in your virtual environment. Try 'pip install -r requirements.txt'.", file=sys.stderr)
except Exception as e:
    print(f"DEBUG_SETTINGS: An unexpected error occurred in settings debug block: {e}", file=sys.stderr)

# Check the default_storage AFTER STORAGES and DEFAULT_FILE_STORAGE are expected to be set
try:
    from django.core.files.storage import default_storage
    print(f"DEBUG_SETTINGS: Django's default_storage is: {default_storage.__class__.__name__} from {default_storage.__class__.__module__}", file=sys.stderr)
    if not hasattr(default_storage, 'url'):
        print(f"DEBUG_SETTINGS: Django's default_storage DOES NOT have 'url' method!", file=sys.stderr)
except Exception as e:
    print(f"DEBUG_SETTINGS: Error checking default_storage: {e}", file=sys.stderr)

# --- END DEBUGGING BLOCK FOR BUNNYSTORAGE ---

# MEDIA_URL should point to your CDN Pull Zone for files uploaded via Django's storage system
# Note: 'media/' will be a subfolder in your Bunny Storage Zone
MEDIA_URL = BUNNY_PULL_ZONE_URL



# Your existing STORAGES setting might look like this:
STORAGES = {
    # Add this for static files:
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}