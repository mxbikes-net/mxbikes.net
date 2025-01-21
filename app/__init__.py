import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from .models import db  # Import db from models instead of extensions

migrate = Migrate()

def create_app(test_config=None, template_folder=None, instance_path=None):
    app = Flask(__name__, instance_relative_config=True)
    if instance_path:
        app.instance_path = instance_path
    if template_folder:
        app.template_folder = template_folder

    app.config.from_object(Config)  # Load config from Config class instead of env variable

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Check for missing config values before registering blueprints
    required_configs = ['SQLALCHEMY_DATABASE_URI', 'SECRET_KEY']
    missing_configs = [config for config in required_configs if config not in app.config]
    if missing_configs:
        print(f"Error: Missing configuration values: {missing_configs}")
        return None

    # Define disabled tabs - can be modified based on your requirements
    disabled_tabs = []  # Empty list means no tabs are disabled

    # Import models to ensure they're registered with SQLAlchemy
    from . import models

    # Register blueprints after database initialization
    from .api import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    # Register main routes
    @app.route('/')
    def index():
        return render_template('index.html', disabled_tabs=disabled_tabs)

    @app.route('/bikes')
    def bikes():
        return render_template('bikes.html', disabled_tabs=disabled_tabs)

    @app.route('/tracks')
    def tracks():
        return render_template('tracks.html', disabled_tabs=disabled_tabs)

    @app.route('/downloads')
    def downloads():
        return render_template('downloads.html', disabled_tabs=disabled_tabs)

    @app.route('/rider')
    def rider():
        return render_template('rider.html', disabled_tabs=disabled_tabs)

    @app.route('/ranked')
    def ranked():
        return render_template('ranked.html', disabled_tabs=disabled_tabs)

    @app.route('/championship')
    def championship():
        return render_template('championship.html', disabled_tabs=disabled_tabs)

    # Add error handlers
    @app.errorhandler(500)
    def internal_error(error):
        print(f"500 Error: {error}")  # Log the error
        return render_template('500.html', disabled_tabs=disabled_tabs), 500

    print(f"Instance Path: {app.instance_path}")
    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"Template Folder: {app.template_folder}")

    return app
