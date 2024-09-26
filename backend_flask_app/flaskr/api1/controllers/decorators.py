from flask import jsonify
from functools import wraps
from flask_jwt_extended import get_jwt_identity, jwt_required, JWTManager

def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Ensure the user is authenticated
            jwt_required()(fn)(*args, **kwargs)

            # Check the user's role
            current_user = get_jwt_identity()
            if current_user['role'] != required_role:
                return jsonify(message='Access forbidden: insufficient permissions'), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator
