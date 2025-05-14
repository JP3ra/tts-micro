# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
# from google.oauth2 import service_account
# import os
# import datetime
# import io
# import json

# SCOPES = ['https://www.googleapis.com/auth/drive.file']

# class GoogleDriveAudioManager:
#     def __init__(self):
#         # Load service account JSON from environment variable
#         credentials_dict = json.loads(os.environ['GOOGLE_CREDS_JSON'])
#         self.creds = service_account.Credentials.from_service_account_info(
#             credentials_dict, scopes=SCOPES
#         )
#         self.service = build('drive', 'v3', credentials=self.creds)

#     def upload_audio(self, file_path: str = "output.wav", filename: str = "output.wav"):
#         file_metadata = {
#             'name': filename,
#             'description': f"Uploaded on {datetime.datetime.utcnow()}",
#             'mimeType': 'audio/wav'
#         }
#         media = MediaFileUpload(file_path, mimetype='audio/wav')
#         file = self.service.files().create(
#             body=file_metadata, media_body=media, fields='id, name').execute()
#         print(f"✅ Uploaded '{filename}' to Google Drive with file ID: {file.get('id')}")
#         return file.get('id')

#     def download_audio(self, file_id: str, save_path: str = "downloaded_output.wav"):
#         request = self.service.files().get_media(fileId=file_id)
#         fh = io.FileIO(save_path, 'wb')
#         downloader = MediaIoBaseDownload(fh, request)
#         done = False
#         while not done:
#             status, done = downloader.next_chunk()
#             print(f"⬇️ Download {int(status.progress() * 100)}% complete.")
#         fh.close()
#         print(f"✅ Audio downloaded to {save_path}")

# manager = GoogleDriveAudioManager()

# # Upload
# file_id = manager.upload_audio("output.wav")

# # Download
# manager.download_audio(file_id, "downloaded_output.wav")



from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.oauth2 import service_account
import os
import datetime
import io
import json

SCOPES = ['https://www.googleapis.com/auth/drive.file']

load_dotenv()

class GoogleDriveAudioManager:
    def __init__(self):
        # Load service account JSON from environment variable
        credentials_dict = json.loads(os.environ['GOOGLE_CREDS_JSON'])
        
        # Use the service account directly instead of OAuth flow
        self.creds = service_account.Credentials.from_service_account_info(
            credentials_dict, scopes=SCOPES
        )
        
        # Build the drive service
        self.service = build('drive', 'v3', credentials=self.creds)

    def upload_audio(self, file_path: str = "output.wav", filename: str = "output.wav"):
        file_metadata = {
            'name': filename,
            'description': f"Uploaded on {datetime.datetime.utcnow()}",
            'mimeType': 'audio/wav'
        }
        media = MediaFileUpload(file_path, mimetype='audio/wav')
        file = self.service.files().create(
            body=file_metadata, media_body=media, fields='id, name').execute()
        print(f"✅ Uploaded '{filename}' to Google Drive with file ID: {file.get('id')}")
        return file.get('id')

    def download_audio(self, file_id: str, save_path: str = "downloaded_output.wav"):
        request = self.service.files().get_media(fileId=file_id)
        fh = io.FileIO(save_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"⬇️ Download {int(status.progress() * 100)}% complete.")
        fh.close()
        print(f"✅ Audio downloaded to {save_path}")

#     # Saving the entries in the database
# manager = GoogleDriveAudioManager()
#     # Upload
# file_id = manager.upload_audio("output.wav")

#     # Download
# manager.download_audio(file_id, "downloaded_output.wav")