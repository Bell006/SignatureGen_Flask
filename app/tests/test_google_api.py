import unittest
from unittest.mock import patch, MagicMock
from app.app import app
from app.google_api import GoogleAPI
from datetime import datetime
from app.app_error import AppError

class TestGoogleAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        self.google_api = GoogleAPI()

        self.mock_credentials = MagicMock() 

        self.mock_credentials_info = {
            "spreadsheet_id": "mock_spreadsheet_id"
        }

        self.google_api.credentials_info = self.mock_credentials_info 

    @patch('google.oauth2.service_account.Credentials.from_service_account_info')
    def test_get_credentials(self, mock_from_service_account_info):
        mock_from_service_account_info.return_value = self.mock_credentials  

        credentials = self.google_api.get_credentials()

        self.assertEqual(credentials, self.mock_credentials)
        mock_from_service_account_info.assert_called_once_with(self.google_api.credentials_info)
    
    @patch('gspread.authorize')
    @patch('app.google_api.GoogleAPI.get_credentials')
    def test_get_google_sheet_service(self, mock_get_credentials, mock_authorize):
        mock_get_credentials.return_value = self.mock_credentials  

        mock_gc = MagicMock()
        mock_authorize.return_value = mock_gc 

        gc = self.google_api.get_google_sheet_service()

        self.assertEqual(gc, mock_gc)

        mock_authorize.assert_called_once_with(self.mock_credentials.with_scopes(['https://www.googleapis.com/auth/spreadsheets']))
    
    @patch('app.google_api.build')
    @patch('app.google_api.GoogleAPI.get_credentials')
    def test_get_google_drive_service(self, mock_get_credentials, mock_build):
        mock_get_credentials.return_value = self.mock_credentials  

        mock_drive_service = MagicMock()
        mock_build.return_value = mock_drive_service 

        drive_service = self.google_api.get_google_drive_service()

        self.assertEqual(drive_service, mock_drive_service)
        mock_build.assert_called_once_with('drive', 'v3', credentials=self.mock_credentials)

    @patch('app.google_api.GoogleAPI.get_google_sheet_service')
    def test_add_to_google_sheet(self, mock_get_google_sheet_service):

            mock_gc = MagicMock()
            mock_spreadsheet = MagicMock()
            mock_worksheet = MagicMock()

            mock_get_google_sheet_service.return_value = mock_gc
            mock_gc.open_by_key.return_value = mock_spreadsheet
            mock_spreadsheet.sheet1 = mock_worksheet

            mock_worksheet.get_all_records.return_value = [
                {"Email": "existing@example.com"}
            ]

            data = {
                "email": "test@example.com",
                "name": "Test User",
                "phone": "123456789",
                "department": "IT",
                "city": "Sample City",
                "state": "SC",
                "regional": "South"
            }

            status_code = self.google_api.add_to_google_sheet(data)

            mock_get_google_sheet_service.assert_called_once()
            mock_gc.open_by_key.assert_called_once_with(self.mock_credentials_info["spreadsheet_id"])
            mock_worksheet.get_all_records.assert_called_once()

            current_date = datetime.now().strftime('%d/%m/%Y')
            mock_worksheet.append_row.assert_called_once_with([
                data["email"],
                data["name"],
                data["phone"],
                data["department"],
                data["city"],
                data["state"],
                data["regional"],
                current_date
            ])

            self.assertEqual(status_code, 200)

    @patch('app.google_api.GoogleAPI.get_google_sheet_service')
    def test_add_to_google_sheet_error(self, mock_get_google_sheet_service):
        mock_get_google_sheet_service.side_effect = Exception("Mocked exception")

        data = {
            "email": "test@example.com",
            "name": "Test User",
            "phone": "123456789",
            "department": "IT",
            "city": "Sample City",
            "state": "SC",
            "regional": "South"
        }

        with self.assertRaises(AppError) as context:
            self.google_api.add_to_google_sheet(data)

        self.assertEqual(context.exception.message, "Erro ao adicionar dados à planilha do Google")
        self.assertEqual(context.exception.status_code, 500)

if __name__ == '__main__':
    unittest.main()
