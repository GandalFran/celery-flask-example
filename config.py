import os

# statement for enabling the development environment
DEBUG = True

# author and license information
AUTHOR = 'Francisco Pinto-Santos'
AUTHOR_EMAIL = 'franpintosantos@usal.es'
LICENSE = 'copyright © 2020'

# flask configuration
PORT = 8000
HOST = '0.0.0.0'
TITLE = 'example'
VERSION = '1.0'
APP_NAME = 'example app'
DESCRIPTION = 'a description'

# celery configuration
CELERY_BROKER = 'amqp://'
CELERY_BACKEND = 'amqp://'

# define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

