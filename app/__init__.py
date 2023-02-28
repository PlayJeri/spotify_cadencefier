from flask import Flask
import os
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URI = os.getenv('DATABASE_URI')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv['SECRET_KEY']

    return app