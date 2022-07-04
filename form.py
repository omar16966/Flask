from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# Create a Form Class
class Form(FlaskForm):
    name = StringField("Enter Your Name", validators=[DataRequired(message="Please Enter Your Name.")])
    submit = SubmitField("Submit")


# Create a Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(message="Please Enter Your Name.")])
    email = StringField("Email", validators=[DataRequired(message="Please Enter Your Email.")])
    submit = SubmitField("Submit")