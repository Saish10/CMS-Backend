from app.app import db, ULIDType, logger
from ulid import new as generate_ulid
from sqlalchemy import func

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_active = db.Column(db.Boolean(), server_default="true", index=True)
    created_date = db.Column(db.DateTime(), server_default=func.now())
    updated_date = db.Column(db.DateTime(), server_default=func.now(), server_onupdate=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.id}"


class User(BaseModel):
    __tablename__ = 'user'

    user_id = db.Column(ULIDType, unique=True,index=True, default=lambda: str(generate_ulid()))
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)

    user_auth_tokens = db.relationship(
        'AuthToken', backref='user', foreign_keys='AuthToken.user_id')

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.username}"

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name


    @classmethod
    def create_user(cls, **data):
        try:
            user = cls(**data)
            db.session.add(user)
            db.session.flush()
            logger.info(f"User created successfully: {user.user_id}")
            return True
        except Exception as e:
            logger.error(f"User: Error in create_user - {e}", exc_info=True)
            return False

    @classmethod
    def get_user(cls, **criteria):
        return cls.query.filter_by(**criteria)


class AuthToken(BaseModel):
    __tablename__ = 'auth_token'

    user_id = db.Column(ULIDType, db.ForeignKey('user.user_id'))
    token = db.Column(db.Text(), nullable=True, index=True)

    def __repr__(self):
        return 'Auth Token for user {}'.format(self.user_id)
    
    @classmethod
    def create_auth_token(cls, **data):
        try:
            token = cls(**data)
            db.session.add(token)
            db.session.flush()
            logger.info(f"Token created successfully: {token.id}")
            return True
        except Exception as e:
            logger.error(
                f"AuthToken: Error in create_auth_token - {e}", exc_info=True)
            return False


