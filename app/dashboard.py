from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from flask_login import login_required, current_user
from dateutil.relativedelta import relativedelta
from app.models import db, Measurement, User
from app.forms import (
    ImperialMeasurementForm,
    MetricMeasurementForm,
    DeleteDataForm
)

import pandas as pd
import plotly
import plotly.graph_objects as go
# import plotly.express as px
import json


charts = Blueprint(
    'charts',
    __name__
)


@charts.route("/", methods=['GET', 'POST'])
@login_required
def home():
    """TODO: Add function doc"""

    if not session.get('system'):
        session['system'] = 'metric'

    if current_user.gender.id == 1:
        df = pd.read_excel('datasets/bmi4age-datatables.xlsx', sheet_name=0)
    else:
        df = pd.read_excel('datasets/bmi4age-datatables.xlsx', sheet_name=1)

    percentiles = [
        '3rd', '5th', '10th', '25th', '50th',
        '75th', '85th', '90th', '95th', '97th'
    ]

    fig = go.Figure()

    for pcent in percentiles:
        fig.add_trace(go.Scatter(
            x=df['Age'],
            y=df[pcent],
            mode='lines',
            name=pcent
        ))

    fig.update_layout(
        title=f"Chart for {current_user.name}",
        template="plotly_white",
        xaxis_title="Age in Months",
        yaxis_title="BMI",
        height=650
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("index.html", graphJSON=graphJSON)


@charts.route("/add-measurement/<system>", methods=["GET", "POST"])
@login_required
def add_measurement(system):
    """
    BMI Calculator KG = Weight (kg) / Height (m)²
    BMI = [Weight (lbs) / Height (inches)²] x 703
    """

    session['system'] = system

    if session['system'] == 'imperial':
        form = ImperialMeasurementForm()

        def calculate_bmi(height, weight):
            return 703 * float(weight)/(float(height) ** 2)
    else:
        form = MetricMeasurementForm()

        def calculate_bmi(height, weight):
            return float(weight)/((float(height)/100) ** 2)

    if form.validate_on_submit():
        height = form.height.data
        weight = form.weight.data
        date = form.date.data
        bmi = calculate_bmi(height, weight)

        new_measurement = Measurement(
            user_id=current_user.id,
            bmi=bmi,
            timestamp=date
        )
        db.session.add(new_measurement)
        db.session.commit()

        flash('Measurement successfully added')

        return redirect("/")
    else:
        return render_template("measurement.html", form=form)


@charts.route("/manage-data", methods=["GET"])
@login_required
def manage_data():
    form = DeleteDataForm()
    measurements = db.session.execute(
        db.select(Measurement).filter_by(user_id=current_user.id)
    ).scalars()

    return render_template(
        "manage-data.html",
        form=form,
        data=measurements
    )


@charts.route("/delete-data/<id>", methods=["POST"])
@login_required
def delete_data(id):
    if request.method == "POST":
        table_entry = db.session.execute(
            db.select(Measurement).filter_by(id=id)
        ).scalar()
        db.session.delete(table_entry)
        db.session.commit()
        return redirect(url_for('charts.manage_data'))
    else:
        return redirect("/")
