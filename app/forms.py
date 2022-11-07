from flask_wtf import FlaskForm
from wtforms import DecimalField, DateField, SelectField, SubmitField, StringField, PasswordField  # NOQA
from wtforms.validators import DataRequired, Email, EqualTo, Length

# TODO: Go through WTFOrms and see if I can improve on validations
# TODO: Add Recaptcha to registration and maybe login


class MeasurementForm(FlaskForm):
    date = DateField(
        'Date of Measurement',
        [DataRequired()]
    )
    height = DecimalField(
        'Height (cm)',
        [DataRequired()]
    )
    weight = DecimalField(
        'Weight (kg)',
        [DataRequired()]
    )
    submit = SubmitField('Add Measurement')


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        [DataRequired()]
    )
    gender = SelectField(
        'Gender',
        [DataRequired()],
        choices=[
            ('Male', 'male'),
            ('Female', 'female'),
        ]
    )
    birthday = DateField(
        'Your Birthday',
        [DataRequired()]
    )
    email = StringField(
        'Email',
        validators=[
            Length(min=6),
            Email(message='Enter a valid email address.'),
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            Length(min=6, message='Select a stronger password'),
            DataRequired()
        ]
    )
    confirmation = StringField(
        'Confirm Your Password',
        validators=[
            EqualTo('password', message='Passwords must match'),
            DataRequired()
        ]
    )
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Enter a valid email.')
        ]
    )
    password = PasswordField(
        'Password',
        [DataRequired()]
    )
    submit = SubmitField('Login')
