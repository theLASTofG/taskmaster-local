import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from src.models.user import db
from src.models.task import Task, TaskApplication
from src.models.review import Review
from src.models.message import Message
from src.models.payment import Payment
from src.routes.auth import auth_bp
from src.routes.tasks import tasks_bp
from src.routes.users import users_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'  # Change this in production

# Enable CORS for all routes
CORS(app)

# Initialize JWT
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(tasks_bp, url_prefix='/api/tasks')
app.register_blueprint(users_bp, url_prefix='/api/users')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()
    
    # Create demo users if they don't exist
    from src.models.user import User
    if not User.query.filter_by(email='cliente@demo.com').first():
        demo_client = User(
            email='cliente@demo.com',
            first_name='Maria',
            last_name='Silva',
            phone='(11) 99999-9999',
            bio='Cliente demo para testes',
            is_tasker=False
        )
        demo_client.set_password('123456')
        db.session.add(demo_client)
    
    if not User.query.filter_by(email='tasker@demo.com').first():
        demo_tasker = User(
            email='tasker@demo.com',
            first_name='João',
            last_name='Santos',
            phone='(11) 88888-8888',
            bio='Tasker experiente em montagem e reparos',
            is_tasker=True,
            rating=4.8,
            total_tasks_completed=23
        )
        demo_tasker.set_password('123456')
        db.session.add(demo_tasker)
    
    db.session.commit()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
