from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,static_url_path='/src/static/', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///donaciones.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
from src.routes import *
