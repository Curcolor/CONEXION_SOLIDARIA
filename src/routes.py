from src import app
from flask import render_template

@app.route('/')
@app.route('/src/templates/index.html')
def home():
    return render_template('index.html')

@app.route('/src/templates/pages/html/registro.html')
def registro():
    return render_template('pages/html/registro.html')

@app.route('/src/templates/pages/html/login.html')
def login():
    return render_template('pages/html/login.html')

@app.route('/src/templates/pages/html/donar.html')
def donar():
    return render_template('pages/html/donar.html')

@app.route('/src/templates/pages/html/perfil.html')
def perfil():
    return render_template('pages/html/perfil.html')

@app.route('/src/templates/pages/html/proyectos.html')
def proyectos():
    return render_template('pages/html/proyectos.html')

@app.route('/src/templates/pages/html/recibir.html')
def recibir():
    return render_template('pages/html/recibir.html')

@app.route('/src/templates/pages/html/nuevaOR.html')
def nuevaOR():
    return render_template('pages/html/nuevaOR.html')

@app.route('/src/templates/pages/html/organizaciones.html')
def organizaciones():
    return render_template('pages/html/organizaciones.html')

