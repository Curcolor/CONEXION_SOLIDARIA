from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,static_url_path='/src/static/', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tu_base_de_datos.db'
db = SQLAlchemy(app)
from src.routes import *
