import flask_wtf
import wtforms
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileAllowed
class AddItemForm(flask_wtf.FlaskForm):
    title = wtforms.StringField("title", validators=[DataRequired()])
    price = wtforms.IntegerField("price", validators=[DataRequired()])
    about = wtforms.TextAreaField("about", validators=[DataRequired()])
    category = wtforms.StringField("category", validators=[DataRequired()])
    image = wtforms.FileField("image", validators=[FileRequired(), FileAllowed(["jpg", "png", "img", "jpeg", "bmp"])])