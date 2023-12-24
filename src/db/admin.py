from flask_admin.contrib.sqla import ModelView

from app.app import admin, db
from .models import User


admin.add_view(ModelView(User, db.session))