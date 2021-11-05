import re
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required, Email, Length, ValidationError, EqualTo


def character_check(form, field):
    excluded_chars = "* ? ! ' ^ + % & / ( ) = } ] [ { $ # @ < >"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(
                f"Character {char} is not allowed.")


def format_check(form, field):
    valid = 0
    phone = field.data
    number = '{}{}{}'.format(phone[0:4], phone[5:8], phone[9:13])
    for i in number:
        if i != "-":
            valid += 1
    if valid != 11:
        raise ValidationError("Phone must be of the form XXXX-XXX-XXXX")


class LoginForm(FlaskForm):
    email = StringField(validators=[Required(), Email()])
    password = PasswordField(validators=[Required()])
    pin = StringField(validators=[Required(), Length(min=6, max=6, message='Pin must be 6 digits')])
    submit = SubmitField()


class RegisterForm(FlaskForm):
    email = StringField(validators=[Required(), Email()])
    firstname = StringField(validators=[Required(), character_check])
    lastname = StringField(validators=[Required(), character_check])
    phone = StringField(validators=[Required(), format_check])
    password = PasswordField(validators=[Required(), Length(min=6, max=12, message='Password must be between 6 and 12 '
                                                                                   'characters in length.')])
    confirm_password = PasswordField(validators=[Required(), EqualTo('password', message='Both password fields must '
                                                                                         'be equal!')])
    pin_key = StringField(
        validators=[Required(), Length(min=32, max=32, message='Pin must have exactly 32 characters')])
    submit = SubmitField(validators=[Required()])

    def validate_password(self, password):
        p = re.compile(r'(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[@$!%*?&])')
        if not p.match(self.password.data):
            raise ValidationError("Password must contain at least 1 digit, 1 uppercase, 1 lowercase letter and 1 "
                                  "special character.")
