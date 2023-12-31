from flask import Flask
from flask_restx import Api, apidoc
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_jwt_extended import JWTManager
from datetime import datetime
from sqlalchemy.types import TypeDecorator, CHAR
from .settings import DEBUG, LOG_DIR
import os
import logging

class ULIDType(TypeDecorator):
    impl = CHAR(26)
    cache_ok = True
    def process_bind_param(self, value, dialect):
        if value is not None:
            return str(value)

    def process_result_value(self, value, dialect):
        if value is not None:
            return value

url_prefix = '/worklog'
app = Flask(__name__)
app.config.from_pyfile('settings.py')
app.debug = DEBUG
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)
admin = Admin(app, template_mode='bootstrap4')


serializer = Marshmallow(app)
apidoc.apidoc.url_prefix = url_prefix
swagger_api = Api(app,
                version='v1.0',
                title='WORKLOG',
                description="WORKLOG API's",
                doc=f'/',
                security='Bearer',
                authorizations={'Bearer': {'type': 'apiKey', 'in': 'header',
                                            'name': 'Authorization'}},
                prefix=url_prefix,
                default_label=None,
                default="API's",
                )


logger = logging.getLogger(__name__)
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

log_file = os.path.join(LOG_DIR, 'worklog.log')
app_handler = logging.FileHandler(log_file)
app_handler.setLevel(logging.DEBUG)
logger.addHandler(app_handler)


from api.urls import *
from db.admin import *
