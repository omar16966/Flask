from flask_wtf import FlaskForm
# import pymysql
from wtforms.widgets import TextArea
from wtforms import (
    StringField,
    SubmitField,
    PasswordField,
    BooleanField,
    ValidationError,
)
from wtforms.validators import DataRequired, EqualTo, Length

# Create a Form Class
class Form(FlaskForm):
    name            = StringField("Enter Your Name", validators=[DataRequired(message="Please Enter Your Name.")])
    submit          = SubmitField("Submit")

# Create a Form Class
class UserForm(FlaskForm):
    name            = StringField("Name", validators=[DataRequired(message="Please Enter Your Name.")])
    email           = StringField("Email", validators=[DataRequired(message="Please Enter Your Email.")])
    password_hash   = PasswordField("Password",validators=[DataRequired(),EqualTo("password_hash2", message="Passwords Must Match!"),])
    password_hash2  = PasswordField("Confirm Password", validators=[DataRequired()])
    favorite_color  = StringField("color")
    submit          = SubmitField("Submit")

class PassForm(FlaskForm):
    email           = StringField("Email", validators=[DataRequired(message="Please Enter Your Email.")])
    password_hash   = PasswordField("Password", validators=[DataRequired(message="Please Enter Your Password.")])
    submit          = SubmitField("Submit")

class PostForm(FlaskForm):
    title           = StringField("Title", validators=[DataRequired(message="Please Enter The Title.")])
    content         = StringField("Content", validators=[DataRequired(message="Please Enter The Content.")], widget=TextArea())
    author          = StringField("Author", validators=[DataRequired(message="Please Enter The Author Name.")])
    slug            = StringField("Slug", validators=[DataRequired(message="Please Enter The Slug.")])
    submit          = SubmitField("Submit")
