from flask import Flask
from flask_restx import Api, apidoc
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_admin import Admin, AdminIndexView
from datetime import datetime
from sqlalchemy.types import TypeDecorator, CHAR
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

bcrypt = Bcrypt(app)

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
                authorizations={'Bearer': {'type': 'apiKey', 'in': 'header',
                                            'name': 'Authorization'}},
                prefix=url_prefix,
                default_label=None,
                default="API's",
                )

current_time = datetime.now()

logger = logging.getLogger(__name__)


from api.urls import *