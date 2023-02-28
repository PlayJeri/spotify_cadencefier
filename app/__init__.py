from flask import Flask
from dotenv import load_dotenv
from .routes import routes
import os

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY

    app.register_blueprint(routes)

    return app

