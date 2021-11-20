##Google Drive API
from Google import Create_Service

CLIENT_SECRET_FILE = 'secrets_DO_NOT_PUSH.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)

folder_names = ['Joe','John','Greg']