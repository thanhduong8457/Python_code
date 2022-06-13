import os
import io
from Google import Create_Service
from googleapicluent.http import MediaIoBaseDownload

CLIENT_SECRET_FILE = 'client_secret_GoogleCloudDemo.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://drive.google.com/drive/folders/']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

file_ids = ['1kL1O0SNCrS9EdOU_Qa6uV5Md5EflmwGa']
file_names = ['ASS-1.pdf']
 
for file_id, file_name in zip(file_ids, file_names):
    service.files().get_media(fileId=file_id)
    
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fd=fh, request=request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print ('Download progress {0}'.format(status.progress() * 100))
    # fh.seek(0)
    
    # with open(os.path.join('./Random Files', file_name), 'wb') as f:
        # f.write(fh.read())
        # f.close()
