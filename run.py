from src import app, db
import os

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5001)))
    with app.app_context():
        db.create_all()  # Crea todas las tablas en la base de datos
        app.run(debug=True)
