from flask_admin.contrib.sqla import ModelView

from app.app import admin, db
from .models import (User, AuthToken
)


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(AuthToken, db.session))