# routes.py
# for rendering api routes
from . import api1
from flask import abort, request, jsonify, current_app
import os
from rembg import remove
import base64
from datetime import datetime
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import csv

import random

# Define folder to save uploaded files to process further
UPLOAD_FOLDER = os.path.join('staticFiles', 'uploads')

# Ensure the directories exist
#os.makedirs(UPLOAD_FOLDER, exist_ok=True)
#os.makedirs(OUTPUT_FOLDER, exist_ok=True)
 
# Define allowed files (for this example I want only csv file)
ALLOWED_EXTENSIONS = {'csv'}


@api1.after_request
def after_request(response):
    '''defining extra headers'''
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PATCH,POST,DELETE,OPTIONS')
    response.headers.add('Content-Type', 'application/json')
    return response


# In-memory user data (replace with database in real use)
users = {}



# Route for use registration
@api1.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        abort(400)
    
    if username in users:
        abort(403)

    # Save the user with hashed password
    users[username] = generate_password_hash(password)
    
    return jsonify({
        'message': 'User registred successfully'
    })

# Route for user login
@api1.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        abort(400)

    # Check if the user exists and the password matches
    user_password_hash = users.get(username)
    if not user_password_hash or not check_password_hash(user_password_hash, password):
        abort(401)
    
    # Create JWT token
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

# Protected route (require validat JWT)
@api1.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    # Get the current user identity for the JWT
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


# Uploade image route
@api1.route('/upload_data', methods=['POST'])
def post_csv_file():
        uploaded_file = request.files.get('image')

        if uploaded_file and uploaded_file.filename != '':
              # Generate unique filenames based on current timestamp
             timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
             original_filename = f'{timestamp}_original.png'
             modified_filename = f'{timestamp}_modified.png'

             # Save the original image to the 'uploads/' directory
             original_filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], original_filename)
             #original_filepath = os.path.join(UPLOAD_FOLDER, original_filename)
             uploaded_file.save(original_filepath)

             # Read the upload image and process (e.g., remove bacground)
             input_image = open(original_filepath, 'rb').read()
             output_image = remove(input_image)

              # Save the modified image to the 'outputs/' directory
             #modified_filepath = os.path.join(OUTPUT_FOLDER, modified_filename)
             modified_filepath = os.path.join(current_app.config['OUTPUT_FOLDER'], modified_filename)
             with open(modified_filepath, 'wb') as f:
                f.write(output_image)

             # Convert images to base64
             encoded_original = base64.b64encode(input_image).decode(('utf-8'))
             encoded_modified = base64.b64encode(output_image).decode(('utf-8'))

            # Return the base64 images in JSON repsonse
             return jsonify({
                'original_image_path': original_filepath,
                'modified_image_path': modified_filepath,
                'original_image': f'data:image/png;base64,{encoded_original}',
                'modified_oimage': f'data:image/png;base64,{encoded_modified}'
            })
        else:
            abort(404)


# error handlers


@api1.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request'
    }), 400

@api1.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'Unauthorized'
    }), 401

@api1.errorhandler(403)
def unauthorized(error):
    return jsonify({
        'success': False,
        'error': 403,
        'message': 'Already exists'
    }), 403


@api1.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
    }), 404


@api1.errorhandler(405)
def not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'method not allowed'
    }), 405


@api1.errorhandler(422)
def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'unprocessable'
    }), 422


@api1.errorhandler(500)
def server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'internal error'
    }), 500