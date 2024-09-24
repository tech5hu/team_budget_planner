from dotenv import load_dotenv  # Import dotenv to load environment variables
import os  # Import os for environment variable handling
from pathlib import Path  # Import Path for easier file path management
import dj_database_url 

# Define the base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent
# Specify the path for the .env file
env_path = BASE_DIR / '.env'

# Load the environment variables from the .env file
load_dotenv(env_path)

# Use environment variables for sensitive settings with defaults
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-secret-key')  # Secret key for Django

# Set DEBUG mode based on the environment variable
DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 't')  # Enable or disable debug mode

# Define allowed hosts for the application
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,teambudgetplanner-fd1be9ca9c90.herokuapp.com').split(',')  # Hosts that can serve the application

# List of installed applications for the Django project
INSTALLED_APPS = [
    'django.contrib.admin',  # Admin site
    'django.contrib.auth',  # Authentication framework
    'django.contrib.contenttypes',  # Content types framework
    'django.contrib.sessions',  # Sessions framework
    'django.contrib.messages',  # Messaging framework
    'django.contrib.staticfiles',  # Static files management
    'budgets',  # Custom application for managing budgets
    'debug_toolbar',  # Debug toolbar for development
]

# Middleware components for processing requests and responses
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Security middleware
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Static files handling
    'django.contrib.sessions.middleware.SessionMiddleware',  # Session management
    'django.middleware.common.CommonMiddleware',  # Common functionalities
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Authentication support
    'django.contrib.messages.middleware.MessageMiddleware',  # Messaging support
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking protection
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # Debug toolbar middleware
    
]

# URL configuration for the project
ROOT_URLCONF = 'team_budget_planner.urls'

# Template settings for rendering HTML
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Template backend
        'DIRS': [BASE_DIR / 'templates'],  # Directories where templates are located
        'APP_DIRS': True,  # Enable loading templates from app directories
        'OPTIONS': {
            'context_processors': [  # Context processors to make variables available in templates
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Configuration for the Django Debug Toolbar
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,  # Prevent debug toolbar from intercepting redirects
}

# Internal IPs for the debug toolbar to work
INTERNAL_IPS = [
    '127.0.0.1',  # Localhost IP
]

# WSGI application configuration for deployment
WSGI_APPLICATION = 'team_budget_planner.wsgi.application'

# Database configuration
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),  # Use DATABASE_URL environment variable for Heroku
        conn_max_age=600,
        ssl_require=True
    )
}

# Password validation settings
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # Validate password against user attributes
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # Ensure minimum password length
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # Check against common passwords
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # Prevent numeric-only passwords
    },
]

# Authentication backends configuration
AUTHENTICATION_BACKENDS = [
    'budgets.backends.EmailBackend',  # Custom email backend for authentication
    'django.contrib.auth.backends.ModelBackend',  # Default model backend
]

# URL redirection settings for login and logout
LOGIN_URL = 'budgets:login'  # URL for login
LOGIN_REDIRECT_URL = 'budgets:home'  # URL to redirect after successful login
LOGOUT_REDIRECT_URL = 'budgets:login'  # URL to redirect after logout

# Session settings
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Database-backed sessions
SESSION_COOKIE_NAME = 'sessionid'  # Name of the session cookie

# Localization settings
LANGUAGE_CODE = 'en-us'  # Default language
TIME_ZONE = 'UTC'  # Default timezone
USE_I18N = True  # Enable internationalization
USE_TZ = True  # Enable timezone support

# Static files settings
STATIC_URL = '/static/'  # URL for serving static files
STATICFILES_DIRS = [BASE_DIR / 'staticfiles']  # Directories where static files are located
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  # Storage backend for static files
STATIC_ROOT = BASE_DIR / 'staticfiles_collected'  # Directory for collected static files

# Email settings for sending emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # SMTP email backend
EMAIL_HOST = 'smtp.gmail.com'  # Email server
EMAIL_PORT = 587  # Email port
EMAIL_USE_TLS = True  # Use TLS for email
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')  # Email address from environment variable
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')  # Email password from environment variable

# Default auto field setting
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # Default field type for auto-generated primary keys
