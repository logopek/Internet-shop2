
import sqlalchemy
from flask_login import UserMixin


from werkzeug.security import generate_password_hash, check_password_hash
from ..db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin

class Item(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'items'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    category = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    image_path = sqlalchemy.Column(sqlalchemy.String, nullable=True)

