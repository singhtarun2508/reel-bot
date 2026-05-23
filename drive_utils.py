from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import io
import os

SCOPES = ['https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_file(
    'credentials.json',
    scopes=SCOPES
)

service = build('drive', 'v3', credentials=credentials)

def list_files(folder_id):
    results = service.files().list(
        q=f"'{folder_id}' in parents and trashed=false",
        fields="files(id, name)"
    ).execute()

    return sorted(results.get('files', []), key=lambda x: x['name'])

def download_file(file_id, filename):
    request = service.files().get_media(fileId=file_id)

    fh = io.FileIO(filename, 'wb')

    downloader = MediaIoBaseDownload(fh, request)

    done = False

    while not done:
        status, done = downloader.next_chunk()

def upload_file(filepath, folder_id):
    file_metadata = {
        'name': os.path.basename(filepath),
        'parents': [folder_id]
    }

    media = MediaFileUpload(filepath, resumable=True)

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    return file.get('id')

def delete_file(file_id):
    service.files().delete(fileId=file_id).execute()