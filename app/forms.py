from flask_wtf import FlaskForm
from wtforms import DecimalField, DateField, SelectField, SubmitField, StringField, PasswordField  # NOQA
from wtforms.validators import DataRequired, Email, EqualTo, Length

# TODO: Add Recaptcha to registration and maybe login


class MeasurementForm(FlaskForm):
    date = DateField(
        'Date of Measurement',
        [DataRequired()]
    )
    submit = SubmitField('Add Measurement')


class ImperialMeasurementForm(MeasurementForm):
    height = DecimalField(
        'Height (inches)',
        [DataRequired()],
        render_kw={"placeholder": "Height (inches)"}
    )
    weight = DecimalField(
        'Weight (lbs)',
        [DataRequired()],
        render_kw={"placeholder": "Weight (lbs)"}
    )


class MetricMeasurementForm(MeasurementForm):
    height = DecimalField(
        'Height (cm)',
        [DataRequired()],
        render_kw={"placeholder": "Height (cm)"}
    )
    weight = DecimalField(
        'Weight (kg)',
        [DataRequired()],
        render_kw={"placeholder": "Weight (kg)"}
    )


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


class RegistrationForm(LoginForm):
    username = StringField(
        'Username',
        [DataRequired()]
    )
    gender = SelectField(
        'Gender',
        [DataRequired()],
        choices=[
            ('MALE', 'Male'),
            ('FEMALE', 'Female'),
        ]
    )
    birthday = DateField(
        'Your Birthday',
        [DataRequired()]
    )
    confirmation = StringField(
        'Confirm Your Password',
        validators=[
            EqualTo('password', message='Passwords must match'),
            DataRequired()
        ]
    )
