import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
SECRET_KEY = os.getenv('SECRET_KEY', 'change-me-in-production')
