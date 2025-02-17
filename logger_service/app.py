from flask import Flask
from routes import bp
import datetime
import uuid


def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)

    return app