from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField
from wtforms.validators import DataRequired, URL, Email, Length
from flask_ckeditor import CKEditorField


# Create a form to register new users
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    profile_pic = FileField('Profile Picture')
    submit = SubmitField("Sign Me Up!")

# Create a form to login existing users
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")


# Create a form to add comments
class CommentForm(FlaskForm):
    comment_text = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")


# Create a form to update profile
class UpdateProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired()])
    profile_pic = FileField('Profile Picture')
    submit = SubmitField("Submit!")


# Create a form to change password
class ChangePasswordForm(FlaskForm):
    password = PasswordField("Enter new password", validators=[DataRequired()])
    submit = SubmitField("Submit!")


class UploadPictureForm(FlaskForm):
    title = StringField('Caption', validators=[DataRequired(), Length(max=100)])
    pics = FileField('Picture')
    submit = SubmitField("Submit!")