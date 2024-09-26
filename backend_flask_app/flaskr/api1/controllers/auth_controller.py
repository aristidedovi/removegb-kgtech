from flask import Blueprint, request, jsonify, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .decorators import role_required

auth_controller = Blueprint('auth_controller', __name__)

# In-memory user data (replace with database in real use)
users = {}

# Example roles dictionary for demonstration
user_roles = {
    'admin_user': 'admin',
    'regular_user': 'user'
}


# Register route
@auth_controller.route('/register', methods=['POST'])
def register():
    print('yes')
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        abort(400)
    
    if username in users:
        abort(403)

    # Save the user with hashed password
    users[username] = generate_password_hash(password)
    
    return jsonify({'message': 'User registered successfully'})

# Login route
@auth_controller.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        abort(400)

    # Check if the user exists and the password matches
    user_password_hash = users.get(username)
    if not user_password_hash or not check_password_hash(user_password_hash, password):
        abort(401)
    
    # Get the user's role (default to 'user' if not found)
    role = user_roles.get(username, 'user')
    
    # Create JWT token
    #access_token = create_access_token(identity=username)
    access_token = create_access_token(identity={'username': username, 'role': role})

    return jsonify(access_token=access_token), 200

# Protected route for admin users olny
@auth_controller.route('/admin', methods=['GET'])
@jwt_required()
@role_required('admin')
def admin_only():
    # Get the current user identity for the JWT
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# Protected route
@auth_controller.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    # Get the current user identity for the JWT
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
