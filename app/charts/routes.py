from flask import Blueprint, render_template

import pandas as pd
import plotly
import plotly.graph_objects as go
# import plotly.express as px
import json


charts = Blueprint(
    'charts',
    __name__,
    template_folder='templates'
)


@charts.route("/", methods=['GET', 'POST'])
def home():
    """TODO: Add function doc"""

    males = pd.read_excel('datasets/bmi4age-datatables.xlsx', sheet_name=0)
    # females = pd.read_excel('datasets/bmi4age-datatables.xlsx', sheet_name=1)

    percentiles = [
        '3rd', '5th', '10th', '25th', '50th',
        '75th', '85th', '90th', '95th', '97th'
    ]
    sex = "Males"

    fig = go.Figure()

    for pcent in percentiles:
        fig.add_trace(go.Scatter(
            x=males['Age'],
            y=males[pcent],
            mode='lines',
            name=pcent
        ))

    fig.update_layout(
        title=f"BMI for Age in {sex}, 2-20 years",
        xaxis_title="Age in Months",
        yaxis_title="BMI",
        height=700
    )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("index.html", graphJSON=graphJSON)
