# tests for the API
import io
import json
from flaskr import create_app
import math
import unittest
import os
from PIL import Image



class TriviaAPI(unittest.TestCase):
    '''
    base class for testing the API
    '''

    # Setup and teardown methods
    # executed before and after each test.
    def setUp(self):
        # creating the application
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        # push the application context with all extentions
        self.app_context.push()
        with self.app.test_client():
            self.client = self.app.test_client()
        
        # Assurez-vous que les dossiers de test existent
        os.makedirs(self.app.config['UPLOAD_FOLDER'], exist_ok=True)
        os.makedirs(self.app.config['OUTPUT_FOLDER'], exist_ok=True)

    def tearDown(self):
        # pop the app context
        self.app_context.pop()
        # Nettoyage après les tests si nécessaire (supprimer les fichiers créés)
        for folder in [self.app.config['UPLOAD_FOLDER'], self.app.config['OUTPUT_FOLDER']]:
            for file in os.listdir(folder):
                os.remove(os.path.join(folder, file))

    def test_remove_background(self):
        # Créer une image factice pour le test
        img = Image.new('RGB', (100, 100), color = (255, 0, 0))  # Image rouge
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)

        # Simuler une requête POST avec une image
        response = self.client.post(
            '/api/v1/remove-background',
            content_type='multipart/form-data',
            data={'images': (img_bytes, 'test_image.png')}
        )

        #print(response)

        # Vérifier que la réponse est un succès
        self.assertEqual(response.status_code, 200)
        
        # Vérifier que la réponse contient les URLs des images traitées
        data = response.get_json()
        self.assertIn('files', data)
        self.assertGreater(len(data['files']), 0)

        # Optionnel: Vérifier que le fichier de sortie existe bien
        #output_image_path = data['files'][0].replace('/static/', 'staticFiles/')
        #self.assertTrue(os.path.exists(output_image_path))

    # def test_register(self):
    #     # Test user registration
    #     response = self.client.post('/api/v1/register', json={
    #         'username': 'testuser2',
    #         'password': 'password123'
    #     })
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b'User registered successfully', response.data)

    
    # def test_register_existing_user(self):
    #     # Register a user and try to register with th same username
    #     self.client.post('/api/v1/register', json={
    #         'username': 'testuser',
    #         'password': 'password123'
    #     })

    #     response = self.client.post('/api/v1/register', json={
    #         'username': 'testuser',
    #         'password': 'password123'
    #     })
    #     self.assertEqual(response.status_code, 403)
    #     self.assertIn(b'Already exists', response.data)

    
    # def test_login(self):
    #     # Register and then login the user
    #     self.client.post('/api/v1/register', json={
    #         'username': 'testuser',
    #         'password': 'password123'
    #     })

    #     response = self.client.post('/api/v1/login', json={
    #         'username': 'testuser',
    #         'password': 'password123'
    #     })
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b'access_token', response.data)
    
    # def test_login_invalid(self):
    #     # Attempt login with wrong credentials
    #     response = self.client.post('/api/v1/login', json={
    #         'username': 'invaliduser',
    #         'password': 'wrongpassword'
    #     })
    #     self.assertEqual(response.status_code, 401)
    #     self.assertIn(b'Unauthorized', response.data)

    # def test_protected_route(self):
    #     # Register, login, and access the protected route
    #     self.client.post('/api/v1/register', json={
    #         'username': 'testuser',
    #         'password': 'password123'
    #     })
    #     login_response = self.client.post('/api/v1/login', json={
    #         'username': 'testuser',
    #         'password': 'password123'
    #     })
    #     access_token = login_response.get_json()['access_token']

    #     # Access the protected route with the valid JWT
    #     response = self.client.get('/api/v1/protected', headers={
    #         'Authorization': f'Bearer {access_token}'
    #     })
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b'logged_in_as', response.data)

    # def test_protected_route_unauthorized(self):
    #     # Try accessing the protected route without a token
    #     response = self.client.get('/api/v1/protected')
    #     self.assertEqual(response.status_code, 401)
    #     self.assertIn(b'Missing Authorization Header', response.data)


    # def test_admin_access(self):
    #     self.client.post('/api/v1/register', json={
    #         'username': 'admin_user',
    #         'password': 'adminpassword'
    #     })

    #     # Login as an admin user
    #     response = self.client.post('/api/v1/login', json={
    #         'username': 'admin_user',
    #         'password': 'adminpassword'
    #     })
    #     assert response.status_code == 200
    #     access_token = response.json['access_token']

    #     # Access the admin-only route
    #     response = self.client.get('/api/v1/admin', headers={
    #         'Authorization': f'Bearer {access_token}'
    #     })
    #     assert response.status_code == 200
    #     assert response.json['logged_in_as']['username'] == 'admin_user'

    # def test_non_admin_access(self):

    #     self.client.post('/api/v1/register', json={
    #         'username': 'regular_user',
    #         'password': 'userpassword'
    #     })

    #     # Login as a regular user
    #     response = self.client.post('/api/v1/login', json={
    #         'username': 'regular_user',
    #         'password': 'userpassword'
    #     })
    #     assert response.status_code == 200
    #     access_token = response.json['access_token']

    #     # Try to access the admin-only route
    #     response = self.client.get('/api/v1/admin', headers={
    #         'Authorization': f'Bearer {access_token}'
    #     })
    #     assert response.status_code == 403
    #     assert response.json['message'] == 'Access forbidden: insufficient permissions'
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()