import datetime
import sqlalchemy
from flask_login import UserMixin
from ..roles.roles import *

from werkzeug.security import generate_password_hash, check_password_hash
from ..db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin

class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    balance = sqlalchemy.Column(sqlalchemy.Integer, default=1000000)
    items = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="")
    role = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=ROLE_USER)
    ban = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)