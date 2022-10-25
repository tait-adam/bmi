from flask import Blueprint, render_template


charts = Blueprint(
    'charts',
    __name__,
    template_folder='templates'
)


@charts.route("/", methods=['GET', 'POST'])
def home():
    """Homepage"""
    return render_template("index.html")
