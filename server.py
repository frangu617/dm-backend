from flask import Flask, send_from_directory
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

# Import controllers
from app.controllers.authentication_controller import authentication_blueprint
from app.controllers.messages_controller import messages_blueprint
from app.controllers.character_controller import character_blueprint
from app.controllers.users_controller import users_blueprint
# Import middleware
from app.middleware.current_user import define_current_user

# Load environment variables
load_dotenv()

# Initialize Flask
app = Flask(__name__, static_folder='client/build')
app.config['MONGO_URI'] = os.getenv('MONGODB_URI')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

# Initialize extensions
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
socketio = SocketIO(app, cors_allowed_origins='*')
CORS(app)

# Register blueprints
app.register_blueprint(authentication_blueprint, url_prefix='/auth')
app.register_blueprint(messages_blueprint, url_prefix='/api/messages')
app.register_blueprint(character_blueprint, url_prefix='/api/characters')
app.register_blueprint(users_blueprint, url_prefix='/users')

# Middleware
app.before_request(define_current_user)

# Serve static files from the React application
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

# @app.route('/protected')
# @jwt_required
# @required_roles('admin')
# def protected():
#     return 'protected'
    
# SocketIO handlers for real-time communication
@socketio.on('connect')
def handle_connection():
    print("A user connected")

@socketio.on('chat message')
def handle_chat_message(message):
    print(f"Message received: {message}")
    socketio.emit('chat message', {'message': message})

@socketio.on('disconnect')
def handle_disconnect():
    print("User disconnected")

# Main entry point
if __name__ == '__main__':
    # Configure port and host dynamically
    port = int(os.getenv('PORT', 5000))
    socketio.run(app, port=port, host='0.0.0.0')
