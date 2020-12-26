from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+f4fh$wn_6)23%_%iuz#k@h3+g5zimtf=a!h%zp)9pmelo3w9^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = ['core']

MIDDLEWARE = [
    'onthespot.middleware.logger.LoggerMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'onthespot.urls'

WSGI_APPLICATION = 'onthespot.wsgi.application'
