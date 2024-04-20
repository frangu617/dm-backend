# Import all your blueprints from the individual controller files
from .authentication_controller import authentication_blueprint
from .messages_controller import messages_blueprint
from .character_controller import character_blueprint
from .users_controller import users_blueprint

# Optionally, you can create a function to register all blueprints at once in your app initialization
def register_blueprints(app):
    app.register_blueprint(authentication_blueprint, url_prefix='/auth')
    app.register_blueprint(messages_blueprint, url_prefix='/api/messages')
    app.register_blueprint(character_blueprint, url_prefix='/api/characters')
    app.register_blueprint(users_blueprint, url_prefix='/users')
