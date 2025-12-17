from pathlib import Path
import os
import dj_database_url
import whitenoise.middleware

BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = 'django-insecure-*)uqh)#%-l=i!un7kgc0jq47_7r=n21jtvj_q3@$v6ex-+r0)j'

"""
    DEBUG = True
    
    ALLOWED_HOSTS = [
    ]
    
    ALLOWED_HOSTS = [
        '127.0.0.1',
        'localhost',
        '10.103.58.224'
    ]
"""







URL_DEFAUT_RENDER = 'postgresql://traino_user:U3zSlRLEh9SZwtcd1pjhBiSvfsgtMBhC@dpg-d5027ef5r7bs73apajeg-a.virginia-postgres.render.com/traino'


IS_RENDER_PRODUCTION = os.environ.get('IS_RENDER_PRODUCTION', 'False') == 'True'
# ----------------------------------------------------------------------


if IS_RENDER_PRODUCTION:
    # Réglages de production sur Render
    DEBUG = False
    
    # Render va injecter le nom d'hôte dans cette variable d'environnement
    RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    
    # Le nom d'hôte externe de Render est requis
    ALLOWED_HOSTS = [RENDER_EXTERNAL_HOSTNAME]

else:
    # Réglages de développement local
    DEBUG = True
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '10.103.58.224']






INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_registration',
    'front',

    'utilisateur',
    'traino_materiel',
    'train',
    'voiture',
    'gare',
    
    
    'voyage',
    'details_voyage',
    'tarification',
    'publication_avis',
    'reservation_paiement',


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'TRAINO_PROJET.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR/'TRAINO_PROJET/templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'TRAINO_PROJET.wsgi.application'


"""


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'TRAINO', 
        'USER': 'postgres', 
        'PASSWORD': 'kalonji082', 
        'HOST': '127.0.0.1', 
        'PORT': '5432', 
        'OPTIONS': {
            
            'options': '-c client_encoding=UTF8', 
        }
    }
}
"""






URL_DEFAUT_RENDER = 'postgresql://traino_user:U3zSlRLEh9SZwtcd1pjhBiSvfsgtMBhC@dpg-d5027ef5r7bs73apajeg-a.virginia-postgres.render.com/traino'

URL_DEFAUT_LOCAL = 'postgresql://postgres:kalonji082@127.0.0.1:5432/TRAINO' 

if DEBUG:
    
    DEFAULT_DB_URL = URL_DEFAUT_LOCAL

else:
    
    DEFAULT_DB_URL = os.environ.get('DATABASE_URL', URL_DEFAUT_RENDER)


DATABASES = {
    'default': dj_database_url.config(
        default=DEFAULT_DB_URL, 
        conn_max_age=600  
    )
}


















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



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True




STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR/'TRAINO_PROJET/static'
]


STATIC_ROOT = BASE_DIR / 'staticfiles' # Rend les fichiers statiques disponibles pour Render



#LOGIN_URL = 'utilisateur/login_comptes'
LOGIN_URL = 'utilisateur:login_comptes'


"""DECONNECTER UN USER APRES UN CERTAINT TEMPS D4INACTIVIT2 DANS L'APPLICATION"""

SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 10 * 60  # 600 secondes
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

"""

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'pinhotelp@gmail.com'
EMAIL_HOST_PASSWORD = 'jgfb xabb dtzs waat'

"""






"""
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'onatratraino@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
"""

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-relay.brevo.com'
EMAIL_PORT = 465                # Port SSL sécurisé
EMAIL_USE_TLS = False           # SSL et TLS ne peuvent pas être True en même temps
EMAIL_USE_SSL = True            # On active le SSL
EMAIL_TIMEOUT = 30
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

DEFAULT_FROM_EMAIL = '9e3b0d001@smtp-brevo.com'

SITE_ID = 2  
ACCOUNT_ACTIVATION_DAYS = 7  

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR/'media'



