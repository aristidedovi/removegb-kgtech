from flask import Blueprint, jsonify
from flask_cors import CORS
from . import api1


#api1 = Blueprint('api1', __name__)
#CORS(api1, resources={r'/api/*': {'origins': '*'}})

# Import controllers
#from .controllers.auth_controller import auth_controller
from .controllers.file_controller import file_controller

# Register controllers with the blueprint
#api1.register_blueprint(auth_controller)
api1.register_blueprint(file_controller)

# Define after_request function
@api1.after_request
def after_request(response):
    '''Defining extra headers'''
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PATCH,POST,DELETE,OPTIONS')
    response.headers.add('Content-Type', 'application/json')
    return response

# Error handlers remain here
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
def forbidden(error):
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
