from flask import Blueprint, render_template, redirect, flash
from flask_login import login_required, current_user
from app.models import db, Measurement
from app.forms import MeasurementForm

import pandas as pd
import plotly
# import plotly.graph_objects as go
import plotly.express as px
import json


charts = Blueprint(
    'charts',
    __name__
)


@charts.route("/", methods=['GET', 'POST'])
@login_required
def home():
    """TODO: Add function doc"""

    # print("**************************************************************")
    # print(f"ID: {record.id}")
    # print(f"Gender: {record.gender.biology}")
    # print(f"Birthday: {record.birthday}")
    # print(f"Measurements: {record.measurements}")
    # for measurement in record.measurements:
    #     print(f"Weight: {measurement.bmi}")
    # print("**************************************************************")

    if current_user.gender.id == 1:
        sex = "Males"
        df = pd.read_excel('datasets/bmi4age-datatables.xlsx', sheet_name=0)
    else:
        sex = "Females"
        df = pd.read_excel('datasets/bmi4age-datatables.xlsx', sheet_name=1)

    percentiles = [
        '3rd', '5th', '10th', '25th', '50th',
        '75th', '85th', '90th', '95th', '97th'
    ]

    fig = px.line(
        df,
        x="Age",
        y=percentiles,
        height=600,
        title=f"BMI for Age in {sex}, 2-20",
        labels={
            "Age": "Age in Months",
            "value": "BMI",
            "variable": "Percentile"
        },
        template="plotly_white"
    )

    fig.update_yaxes(
        showgrid=True
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("index.html", graphJSON=graphJSON)


@charts.route("/add-measurement", methods=["GET", "POST"])
@login_required
def add_measurement():
    """
    BMI Calculator KG = Weight (kg) / Height (m)²
    BMI = [Weight (lbs) / Height (inches)²] x 703
    """
    form = MeasurementForm()
    if form.validate_on_submit():
        height = form.height.data
        weight = form.weight.data
        bmi = float(weight)/((float(height)/100) ** 2)

        new_measurement = Measurement(
            user_id=current_user.id,
            bmi=bmi
        )
        db.session.add(new_measurement)
        db.session.commit()

        flash('Measurement successfully added')

        return redirect("/")
    else:
        return render_template("measurement.html", form=form)
