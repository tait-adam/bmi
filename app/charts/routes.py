from flask import Blueprint, render_template, request, redirect, flash
from app.models import db, User, Measurement

import pandas as pd
import plotly
# import plotly.graph_objects as go
import plotly.express as px
import json


charts = Blueprint(
    'charts',
    __name__,
    template_folder='templates'
)


@charts.route("/", methods=['GET', 'POST'])
def home():
    """TODO: Add function doc"""

    # TODO: Get id from session
    id = 1

    record = db.session.execute(
        db.select(User).filter_by(id=id)
    ).scalar()

    # print("**************************************************************")
    # print(f"ID: {record.id}")
    # print(f"Gender: {record.gender.biology}")
    # print(f"Birthday: {record.birthday}")
    # print(f"Measurements: {record.measurements}")
    # for measurement in record.measurements:
    #     print(f"Weight: {measurement.bmi}")
    # print("**************************************************************")

    if record.gender.id == 1:
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
def add_measurement():
    if request.method == "POST":
        id = 1  # TODO: Get id from session
        height = request.form.get('height')
        weight = request.form.get('weight')
        bmi = float(weight)/((float(height)/100) ** 2)

        # Metric BMI formula
        # BMI Calculator KG = Weight (kg) / Height (m)²
        # Imperial BMI formula
        # BMI = [Weight (lbs) / Height (inches)²] x 703

        new_measurement = Measurement(
            user_id=id,
            bmi=bmi
        )
        db.session.add(new_measurement)
        db.session.commit()

        flash('Measurement successfully added')

        return redirect("/")
    else:
        return render_template("measurement.html")
