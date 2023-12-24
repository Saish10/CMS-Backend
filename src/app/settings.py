import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
DATABASE = {
	'NAME': os.environ.get('DB_NAME'),
	'USER': os.environ.get('DB_USER'),
	'PASSWORD': os.environ.get('DB_PASSWORD'),
	'HOST': os.environ.get('DB_HOST'),
	'PORT': os.environ.get('DB_PORT')
}

SQLALCHEMY_DATABASE_URI = "postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}".format(**DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = bool(os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS'))
FLASK_ADMIN_SWATCH = os.environ.get('FLASK_ADMIN_SWATCH')
DEBUG = bool(os.environ.get('DEBUG'))