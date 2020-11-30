from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, RadioField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Zoom.models import User

class RegestrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4,max=20)])
    email = StringField('Email Adress', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    dept = SelectField(u'Departement', choices=[('Computer Science', 'Computer Science'),('Science and Technology', 'Science and Technology'),('Material Science', 'Material Science')])
    gender = RadioField('Gender', choices=[('Male','Male'),('Female','Female')])
    submit = SubmitField('Register')
    """ Custom Validations """
    # check for duplicate usernames
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken')
    # check for duplicate emails
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already taken')

class LoginForm(FlaskForm):
    email = StringField('Email Adress', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')