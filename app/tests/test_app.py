import unittest
from unittest.mock import patch, MagicMock
from app.app import app, google_api
import json
class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.testing = True
        self.mock_google_api = google_api

    @patch('app.google_api.GoogleAPI.add_to_google_sheet')
    @patch('app.google_api.GoogleAPI.get_google_drive_service')
    def test_create_signature_success(self, mock_get_google_drive_service, mock_add_to_google_sheet):
        mock_drive_service = MagicMock()
        mock_get_google_drive_service.return_value = mock_drive_service

        mock_drive_service.files().create().execute.return_value = {'id': 'mocked_file_id'}
        mock_drive_service.files().get().execute.return_value = {'webContentLink': 'https://mocked_link'}

        data = {
            "email": "test@example.com",
            "name": "Test User",
            'phone': '62982161616',
            "department": "TI",
            "city": "Goiânia",
            "state": "Goiás",
            "regional": ""
        }

        response = self.app.post('/create_signature', 
                            data=json.dumps(data), 
                            content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('image_url', response.get_json())
        self.assertEqual(response.get_json()['image_url'], 'https://mocked_link')

        mock_add_to_google_sheet.assert_called_once_with(data)
        mock_get_google_drive_service.assert_called_once()

    def test_create_email_signature_missing_fields(self):

        data = {
            'email': 'test@example.com',
            'phone': '62982161616',
            'department': 'Engenharia',
            'city': 'Goiânia',
            'state': 'Goiás',
            'regional': 'Centro Oeste'
        }

        response = self.app.post('/create_signature', 
                             data=json.dumps(data), 
                             content_type='application/json')

        # Verifica se o código de status é 400
        self.assertEqual(response.status_code, 400)

        # Verifica a mensagem de erro na resposta
        response_json = json.loads(response.data)
        self.assertEqual(response_json['message'], 'Preencha todos os campos.')

if __name__ == '__main__':
    unittest.main()
