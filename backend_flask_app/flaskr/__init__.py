
import os
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from flask_graphql import GraphQLView
from flask_pymongo import PyMongo
from flask_cors import CORS


#mongo = PyMongo()


def create_app(config=None):
    # create and configure the app
    app = Flask(__name__)

    # Configure JWT
    jwt = JWTManager(app)

    # Allow CORS for all domains or specify certain domains like localhost:3001
    #CORS(app, resources={r"/graphql": {"origins": "http://localhost:3001"}})
    CORS(app, resources={r"/static/*": {"origins": "*"}})

    


    if config == 'development':
        app.config.from_object('config.DevConfig')
    elif config == 'production':
        app.config.from_object('config.ProdConfig')
    elif config == 'testing':
        app.config.from_object('config.TestConfig')
    else:
        raise EnvironmentError(
            'Please specify a valid configuration profile for the application. Possible choices are `development`, `testing`, or `production`')
    # bind all extentions to the app instance
    with app.app_context():
        # import blueprints
        from .api1 import api1
        #from .schema import schema
        #from contoller.error_handle import error_handlers
        # register blueprints
        app.register_blueprint(api1, url_prefix='/api/v1')
        #app.register_blueprint(error_handlers)
        # app.add_url_rule(
        #     '/graphql',
        #     view_func=GraphQLView.as_view(
        #         'graphql',
        #         schema=schema,
        #         graphiql=True
        #     )
        # )
    
        # Initialize PyMongo with the app
        #mongo.init_app(app)


        # force 404 and 405 errors to return a json object if requested from the api blueprint
        @app.errorhandler(404)
        def _handle_404(error):
            if request.path.startswith('/api/v1/'):
                return jsonify({
                    'success': False,
                    'error': 404,
                    'message': 'resource not found'
                }), 404
            else:
                return error

        @app.errorhandler(405)
        def _handle_405(error):
            if request.path.startswith('/api/v1/'):
                return jsonify({
                    'success': False,
                    'error': 405,
                    'message': 'method not allowed'
                }), 405
            else:
                return error
    return app
