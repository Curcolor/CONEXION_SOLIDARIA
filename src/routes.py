from src import app

@app.route('/')
def home():
    return "¡Bienvenido a la plataforma de donaciones!"