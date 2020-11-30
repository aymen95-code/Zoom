from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, RadioField, BooleanField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from flask_login import current_user
from Zoom.models import User

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4,max=20)])
    email = StringField('Email Adress', validators=[DataRequired(), Email()])
    gender = RadioField('Gender', choices=[('Male','Male'),('Female','Female')])
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('update')

    # check for duplicate username + user's username != keyed in username
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken, please choose a different one')
    # Check of duplicate email + user's email != keyed in email
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken, please choose a different one')