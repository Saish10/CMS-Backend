from app.app import serializer
from db.models import User

from marshmallow import fields, Schema, validate

class RegisterSchema(serializer.Schema):
    email = fields.String(required=True)
    username = fields.String(required=True, validate=validate.Length(min=3, max=30))
    password = fields.String(required=True, validate=validate.Length(min=6))
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)

class UserDetailSerializer(serializer.Schema):

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'is_active')