import flask_wtf
import wtforms
from wtforms.validators import DataRequired
class LoginForm(flask_wtf.FlaskForm):
    login = wtforms.StringField("login", validators=[DataRequired()])
    password = wtforms.StringField("password", validators=[DataRequired()])
    remember_me = wtforms.BooleanField("remember_me")