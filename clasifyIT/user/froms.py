from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo,Regexp
from clasifyIT.models import User
from wtforms.validators import ValidationError


class SingupForm(FlaskForm):
    """Registration form."""
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,

               'Username must contain only letters, numbers, dots or underscores') ])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Regexp(
                                                    "^(?=.{8,})(?=.*[1-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[(!@#$%^&*()_+|~\- =\`{}[\]:”;'<>?,.\/, )])(?!.*(.)\1{2,}).+$",
                                                         0, "Password must contain at least 8 chars"
                                                            ", at least one digit, at least one lowercase, at least one uppercase, at leatet one speacial char and without sequencial repeats"
                                                     ), Length(max=16)])
    password2 = PasswordField('Password2',
                              validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email', validators=[DataRequired(), Length(max=64)])
    firstName=StringField('First Name',validators=[DataRequired(), Length(min=4, max=20)])
    lastName=StringField('Last Name',validators=[DataRequired(), Length(min=4, max=20)])
    submit = SubmitField('Sumbit')


class LoginForm(FlaskForm):
    """Login form."""
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=64)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=16)])
    submit = SubmitField('Login')


class OtaloginForm(FlaskForm):
    """Second factor authentication login"""
    token = StringField('Token', validators=[DataRequired(), Length(6, 6)])
    code = StringField('code', validators=[DataRequired(), Length(64, 64)])
    submit = SubmitField('Login')

class RequestResetForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('There is no account with that username. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Regexp(
                                                         "^(?=.{8,})(?=.*[1-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[(!@#$%^&*()_+|~\- =\`{}[\]:”;'<>?,.\/, )])(?!.*(.)\1{2,}).+$",
                                                         0,
                                                         "Password must contain at least 8 chars, at least one digit, at least one lowercase, at least one uppercase, at leatet one speacial char and without sequencial repeats"

                                                     )])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class ChangeUsername(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    confirm_username = StringField('Confirm Username',
                                        validators=[DataRequired(), EqualTo('username')])

    submit = SubmitField('Change user')


class ChangeName(FlaskForm):
    firstName=StringField('First Name',validators=[DataRequired()])
    lastName=StringField('Last Name',validators=[DataRequired()])
    submit = SubmitField('Change name')


class ChangeEmail(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired()])

    submit = SubmitField('Change email')