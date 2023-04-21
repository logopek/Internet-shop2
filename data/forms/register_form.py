import flask_wtf
import wtforms
from wtforms.validators import DataRequired
class RegisterForm(flask_wtf.FlaskForm):
    login = wtforms.StringField("login", validators=[DataRequired()])
    password = wtforms.PasswordField("password", validators=[DataRequired()])
    email = wtforms.EmailField("email", validators=[DataRequired()])