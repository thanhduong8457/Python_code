import os
import io
from Google import Create_Service
from googleapiclient.http import MediaIoBaseDownload

CLIENT_SECRET_FILE = 'client_secret_GoogleCloudDemo.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://drive.google.com/drive/folders/1kL1O0SNCrS9EdOU_Qa6uV5Md5EflmwGa']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

file_ids = ['1KwcYzXAvg1fWrjQBRsVH5tQWVYOtUrVq']
file_names = ['ASS-1.pdf']

for file_id, file_name in zip(file_ids, file_names):
    request = service.files().get_media(fileId=file_id)

    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fd=fh, request=request)
    done = False

    while not done:
        status, done = downloader.next_chunk()
        print('Downloand Progress {0}'.format(status.progress()*100))
        
    fh.seek(0)

    with open(os.path.join('./Ramdom File', file_name), 'wb') as f:
        f.write(fh.read())
        f.close()