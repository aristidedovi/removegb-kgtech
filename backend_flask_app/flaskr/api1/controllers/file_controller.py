import os
import io
import base64
from datetime import datetime
from flask import Blueprint, request, jsonify, abort, current_app, url_for, send_from_directory
from rembg import remove, new_session
from werkzeug.utils import secure_filename
from PIL import Image
import requests


file_controller = Blueprint('file_controller', __name__)

# Define folder to save uploaded files to process further
#UPLOAD_FOLDER = os.path.join('staticFiles', 'uploads')
# OUTPUT_FOLDER = os.path.join('staticFiles', 'outputs')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def make_square(image, size=(500, 500)):
    """Resize image to a square format."""
    # Resize the image while keeping aspect ratio
    image.thumbnail(size)

    # Create a new square image (background)
    square_img = Image.new("RGBA", size, (255, 255, 255, 0))  # Transparent background

    # Paste the resized image onto the square background, centered
    square_img.paste(
        image,
        ((size[0] - image.size[0]) // 2, (size[1] - image.size[1]) // 2)
    )

    return square_img



@file_controller.route('/remove-background', methods=['POST'])
def remove_background():
    if 'images' not in request.files:
        abort(400)

    files = request.files.getlist('images')
    urls = []

    # Process each file
    for file in files:
        if file and allowed_file(file.filename):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            #model_name = "unet" u2netp
            model_name = "unet" 
            rembg_session = new_session(model_name)

            # Read the upload image and process (e.g., remove background)
            input_image = open(file_path, 'rb').read()
            output_image = remove(input_image, session=rembg_session)

            # Convert the byte data to a PIL image
            image = Image.open(io.BytesIO(output_image))

            # Resize the image to a square format
            square_image = make_square(image, size=(500, 500))

            # Save the modified image to the 'outputs/' directory
            modified_filename = f'modified_{timestamp}_{filename}'
            modified_filepath = os.path.join(current_app.config['OUTPUT_FOLDER'], modified_filename)
            square_image.save(modified_filepath, format="PNG")

            # with open(modified_filepath, 'wb') as f:
            #     f.write(output_image)


            image_url = url_for('static', filename=f'outputs/{modified_filename}')
            urls.append(image_url)

    if urls:
        return jsonify({'message': 'Images processed', 'files': urls}), 200

            # Convert images to base64
            #encoded_original = base64.b64encode(input_image).decode('utf-8')
            #encoded_modified = base64.b64encode(output_image).decode('utf-8')

            #return jsonify({'message': 'Images processed', 'files': [url_for('static',filename=filename)]}), 200
            #return jsonify({'message': 'Images processed', 'files': [request.url_root + url_for('static', filename="/images/" + filename)]}), 200


    abort(400)



# @file_controller.route('/create_image', methods=['POST'])
# def create_image():

#     api_key = 'f88631e5-d4f8-4b53-a402-39d656664ebf'
#     template_id = 'aa6d3253-2b7b-468c-85e6-576e20152e0a'

#     url = 'https://api.templated.io/v1/render'
#     headers = {
#     'Content-Type': 'application/json',
#     'Authorization': f'Bearer {api_key}'
#     }

#     data = {
#         'template': template_id,
#         'layers': {
#             'text-1': {
#                 'text': 'Aristide'
#             },
#             'text-2': {
#                 'text': '@aris'
#             },
#             'text-4': {
#                 'text': ' Je suis ce que je suis!'
#             },
#             'text-2-2': {
#                 'text': 'make by aris'
#             }
#         }
#     }

#     response = requests.post(url, json=data, headers=headers)
#     return response

    # if response.status_code == 200:
    #     print('Render request accepted.')
    # else:
    #     print('Render request failed. Response code:', response.status_code)
    #     print(response.text)

@file_controller.route('/upload_data', methods=['POST'])
def post_csv_file():
    uploaded_file = request.files.get('image')

    if uploaded_file and uploaded_file.filename != '':
        # Generate unique filenames based on current timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        original_filename = f'{timestamp}_original.png'
        modified_filename = f'{timestamp}_modified.png'

        # Save the original image to the 'uploads/' directory
        original_filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], original_filename)
        uploaded_file.save(original_filepath)

        # Read the upload image and process (e.g., remove background)
        input_image = open(original_filepath, 'rb').read()
        output_image = remove(input_image)

        # Save the modified image to the 'outputs/' directory
        modified_filepath = os.path.join(current_app.config['OUTPUT_FOLDER'], modified_filename)
        with open(modified_filepath, 'wb') as f:
            f.write(output_image)

        # Convert images to base64
        encoded_original = base64.b64encode(input_image).decode('utf-8')
        encoded_modified = base64.b64encode(output_image).decode('utf-8')

        # Return the base64 images in JSON response
        return jsonify({
            'original_image_path': original_filepath,
            'modified_image_path': modified_filepath,
            'original_image': f'data:image/png;base64,{encoded_original}',
            'modified_image': f'data:image/png;base64,{encoded_modified}'
        })
    else:
        abort(404)
