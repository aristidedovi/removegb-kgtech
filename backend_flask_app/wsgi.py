# entry file to the application
from flaskr import create_app
from os import environ
from flask import send_from_directory, jsonify


# creating the app with configuration durrived from FLASK_CONFIG environment variable, or fall back to development.
config = environ.get('FLASK_CONFIG') or 'development'
app = create_app(config)

# @app.route('/static/<filemane>', methods=['GET', 'POST'])
# def serve_static(filename):
#     #return True
#     #filename="outputs/modified_20240919_153453_1695287003504.jpg"
#     #return send_from_directory('static', filename)
#     return jsonify({'message': 'Images processed', 'filename': filename})


# finally, run the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)