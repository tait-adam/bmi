from flask import Flask, render_template
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Globally accessible libraries
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    """Initialise the core application"""

    # Configure application
    app = Flask(__name__)
    app.config.from_object('config.Config')

    with app.app_context():
        register_blueprints(app)
        initialise_extensions(app, db)
        configure_logging(app)
        register_error_handlers(app)

    return app


# Helper Functions
def register_blueprints(app):
    from app.charts import routes
    app.register_blueprint(routes.charts)


def initialise_extensions(app, db):
    db.init_app(app)
    migrate.init_app(app, db)
    Session(app)


def configure_logging(app):
    # https://towardsdatascience.com/how-to-set-up-a-production-grade-flask-application-using-application-factory-pattern-and-celery-90281349fb7a
    pass


def register_error_handlers(app):
    """
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
    1xx informational response
    2xx success
    3xx redirection
    4xx client error
    5xx server error
    """

    @app.errorhandler(404)
    def page_not_found(e):
        pass
