# app/__init__.py
from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize extensions at the module level
mongo = PyMongo()
bcrypt = Bcrypt()
jwt = JWTManager()
socketio = SocketIO()
cors = CORS()

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, static_folder='../client/build')
    app.config['MONGO_URI'] = os.getenv('MONGODB_URI')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

    # Bind extensions to the app
    mongo.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins='*')
    cors.init_app(app)
    
    CORS(app, supports_credentials=True)
    
    # Import and register blueprints
    from .controllers.authentication_controller import authentication_blueprint
    from .controllers.messages_controller import messages_blueprint
    from .controllers.character_controller import character_blueprint
    from .controllers.users_controller import users_blueprint
    app.register_blueprint(authentication_blueprint, url_prefix='/auth')
    app.register_blueprint(messages_blueprint, url_prefix='/api/messages')
    app.register_blueprint(character_blueprint, url_prefix='/api/characters')
    app.register_blueprint(users_blueprint, url_prefix='/users')

    # Register middleware
    from .middleware.current_user import define_current_user
    app.before_request(define_current_user)

    return app

# Optionally, expose socketio for external use
def get_socketio():
    return socketio
