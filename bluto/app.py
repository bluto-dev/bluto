"""The app module, containing the app factory function."""

import logging
import sys

from flask import Flask
from flask import render_template

from bluto import public
from bluto.extensions import cache
from bluto.extensions import debug_toolbar

# Use cdn if in production
STATIC_URL_PATH = "/static"

def create_app(config_object="bluto.settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0], static_url_path=STATIC_URL_PATH)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    configure_logger(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    cache.init_app(app)
    debug_toolbar.init_app(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template(f"{error_code}.html"), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)

app = Flask(__name__, static_url_path=STATIC_URL_PATH)
