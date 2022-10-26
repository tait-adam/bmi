from flask import Blueprint, render_template

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

    df = pd.read_excel('datasets/bmi4age-datatables.xlsx', sheet_name=0)
    # df = pd.read_excel('datasets/bmi4age-datatables.xlsx', sheet_name=1)

    sex = "Males"
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
