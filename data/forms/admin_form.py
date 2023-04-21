import flask_wtf
import wtforms
from wtforms.validators import DataRequired
class AdminForm(flask_wtf.FlaskForm):
    select = wtforms.SelectField("select", validators=[DataRequired()], choices=["Ban","Unban", "Make Moderator", "Make Admin"])
    user_id = wtforms.IntegerField("user_id", validators=[DataRequired()])