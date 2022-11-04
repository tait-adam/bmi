from flask_wtf import FlaskForm
from wtforms import DecimalField, DateField, SubmitField
from wtforms.validators import DataRequired


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
