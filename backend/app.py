# backend/app.py
from database import init_app, db
from models import User, Task 
from routes.auth import auth_bp
from routes.tasks import tasks_bp

app = init_app()

# --- Registrar blueprints aquí
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(tasks_bp, url_prefix='/api')

@app.route("/")
def home():
    return "To-Do Pro API funcionando 🚀"

if __name__ == "__main__":
    app.run(debug=False)
