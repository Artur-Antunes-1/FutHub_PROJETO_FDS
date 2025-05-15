"""
Django settings for project.

Prontos para produção e para o Azure App Service.
Valores sensíveis são lidos de variáveis de ambiente.
"""

from pathlib import Path
import os
from django.core.management.utils import get_random_secret_key

# ---------------------------------------------------------------------------
# Diretórios base                                                             
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Segurança                                                                   
# ---------------------------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", get_random_secret_key())
# DEBUG = os.getenv("DEBUG", "False").lower() in {"1", "true", "yes"}
# DEBUG = True
DEBUG = False
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "futhub-webapp.azurewebsites.net",
    "169.254.131.2",        # para o probe sem porta
    "169.254.131.2:8000",   # para o probe COM porta
    # opcionalmente, em teste:
    # "*"                     # libera qualquer host (remova depois!)
]

# Confiança de CSRF (útil para Azure)
CSRF_TRUSTED_ORIGINS = [f"https://{h}" for h in ALLOWED_HOSTS if "." in h]

# ---------------------------------------------------------------------------
# Banco de dados (SQLite em dev, persistente no Azure em produção)
# ---------------------------------------------------------------------------
if os.getenv("WEBSITE_SITE_NAME"):   # estamos no Azure
    RUNTIME_DB_DIR = Path("/home/site/data")
    RUNTIME_DB_DIR.mkdir(parents=True, exist_ok=True)
    DB_PATH = RUNTIME_DB_DIR / "db.sqlite3"
else:                                # dev local
    DB_PATH = Path(__file__).resolve().parent.parent / "db.sqlite3"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": str(DB_PATH),
    }
}

# ---------------------------------------------------------------------------
# Aplicações                                                                  
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",   # staticfiles em dev sem collectstatic
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # apps do projeto
    "core",
]

# ---------------------------------------------------------------------------
# Middleware                                                                  
# ---------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # serve arquivos estáticos
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "project.wsgi.application"

# ---------------------------------------------------------------------------
# Autenticação                                                                
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/home"
LOGOUT_REDIRECT_URL = "/home"

# ---------------------------------------------------------------------------
# Internacionalização                                                        
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Arquivos estáticos                                                         
# ---------------------------------------------------------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "core" / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ---------------------------------------------------------------------------
# Campos padrão                                                               
# ---------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"