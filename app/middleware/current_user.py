from flask import g, jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from app.data_access.user import find_user_by_id
import os

def define_current_user():
    """
    Function to be used as a before_request hook to set the current user.
    """
    try:
        verify_jwt_in_request(optional=True)
        current_user_id = get_jwt_identity()
        if current_user_id:
            user = find_user_by_id(current_user_id)
            if user:
                g.current_user = user
            else:
                return jsonify({"error": "User not found"}), 401
    except NoAuthorizationError:
        # It's fine if there's no JWT, as it's optional
        pass

def jwt_required(fn):
    """Decorator that can be used to protect a route with JWT."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except NoAuthorizationError:
            return jsonify(error="Missing or invalid token"), 401
    return wrapper

def required_roles(*allowed_roles):
    """Decorator to enforce required roles."""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if not g.get('current_user'):
                return jsonify(error="Unauthorized"), 401
            if g.current_user.get('role') not in allowed_roles:
                return jsonify(error="Forbidden: Insufficient permissions"), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

class NoAuthorizationError(Exception):
    pass
