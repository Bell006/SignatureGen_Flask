import os
from google.oauth2 import service_account
import gspread
from googleapiclient.discovery import build
from app.app_error import AppError
from datetime import datetime

class GoogleAPI:
    def __init__(self):
        self.credentials_info = {
            "type": os.getenv('TYPE'),
            "project_id": os.getenv('PROJECT_ID'),
            "private_key_id": os.getenv('PRIVATE_KEY_ID'),
            "private_key": os.getenv('PRIVATE_KEY'),
            "client_email": os.getenv('CLIENT_EMAIL'),
            "client_id": os.getenv('CLIENT_ID'),
            "auth_uri": os.getenv('AUTH_URI'),
            "token_uri": os.getenv('TOKEN_URI'),
            "auth_provider_x509_cert_url": os.getenv('AUTH_PROVIDER_X509_CERT_URL'),
            "client_x509_cert_url": os.getenv('CLIENT_X509_CERT_URL'),
            "universe_domain": "googleapis.com",
            "spreadsheet_id": os.getenv('GOOGLE_SHEET_ID'),
            "google_drive_folder_id": os.getenv('GOOGLE_DRIVE_FOLDER_ID')
        }

    def get_credentials(self):
        try:
            credentials = service_account.Credentials.from_service_account_info(self.credentials_info)
            return credentials
        except Exception as e:
            print(f"Erro ao obter credenciais: {e}")
            raise AppError("Erro ao obter credenciais do Google", 500)

    def get_google_sheet_service(self):
        try:
            scopes = ['https://www.googleapis.com/auth/spreadsheets']
            credentials = self.get_credentials()

            credentials = credentials.with_scopes(scopes)
            gc = gspread.authorize(credentials)

            return gc
        except Exception as e:
            print(f"Erro ao autorizar Google Sheets: {e}")
            raise AppError("Erro ao conectar com Google Sheets", 500)

    def get_google_drive_service(self):
        credentials = self.get_credentials()
        try:
            drive_service = build('drive', 'v3', credentials=credentials)
            return drive_service
        except Exception as e:
            print(f"Erro ao autorizar Google Drive: {e}")
            raise AppError("Erro ao conectar com Google Drive", 500)
    
    def add_to_google_sheet(self, data):
        try:
            gc = self.get_google_sheet_service()

            spreadsheet_id = self.credentials_info["spreadsheet_id"]
            spreadsheet = gc.open_by_key(spreadsheet_id)

            worksheet = spreadsheet.sheet1

            email = data.get('email')
            existing_rows = worksheet.get_all_records()

            row_to_delete = None
            for index, row in enumerate(existing_rows):
                if row['Email'].strip().lower() == email.strip().lower():
                    row_to_delete = index + 2  
                    break

            if row_to_delete:
                worksheet.delete_rows(row_to_delete)

            current_date = datetime.now().strftime('%d/%m/%Y')

            worksheet.append_row([
                data['email'],
                data['name'],
                data['phone'],
                data['department'],
                data['city'],
                data['state'],
                data['regional'],
                current_date
            ])

            return 200
        except Exception as e:
            print(f"Erro ao adicionar dados à planilha: {e}")
            raise AppError("Erro ao adicionar dados à planilha do Google", 500)
    
    
    
