from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def drive():
    '''
    Retorna un recurso a la API de Google Drive. Este recurso nos permitira acceder a los archivos guardados
    en Drive. De esta manera se podra listarlos y cambiar los permisos de los mismo cuando fuera necesario.
    
    Utilizando las credenciales obtenidas para usar la API de Google Drive, almacenadas en credentials_drive.json
    genera un token por usuario, una vez que este acepta los permisos requeridos en el scope. Este token sera
    almacenado en token_drive.json
    El token sirve para que el usuario no tenga que aceptar los permisos cada vez que accede a la app.
    Si se quiere cambiar de usuario se debe borrar el archivo token_drive.json
    '''    
    SCOPES_DRIVE = ['https://www.googleapis.com/auth/drive']
    creds = None
    if os.path.exists('token_drive.json'):
        creds = Credentials.from_authorized_user_file('token_drive.json', SCOPES_DRIVE)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials_drive.json', SCOPES_DRIVE)
            creds = flow.run_console()
        with open('token_drive.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('drive', 'v3', credentials=creds)
        return service
    except HttpError as error:
        print('Ocurrio un error al generar el recurso a la API Drive: %s' % error)

        
def gmail():
    '''
    Retorna un recurso a la API de Gmail. Este recurso nos permitira enviar mails desde Gmail.
    
    Utilizando las credenciales obtenidas para usar la API de Gmail, almacenadas en credentials_gmail.json
    genera un token por usuario, una vez que este acepta los permisos requeridos en el scope. Este token sera
    almacenado en token_gmail.json
    El token sirve para que el usuario no tenga que aceptar los permisos cada vez que accede a la app.
    Si se quiere cambiar de usuario se debe borrar el archivo token_gmail.json
    '''
    SCOPES_GMAIL = ['https://www.googleapis.com/auth/gmail.send']
    creds = None
    if os.path.exists('token_gmail.json'):
        creds = Credentials.from_authorized_user_file('token_gmail.json', SCOPES_GMAIL)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials_gmail.json', SCOPES_GMAIL)
            creds = flow.run_console()
        with open('token_gmail.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except HttpError as error:
        print('Ocurrio un error al generar el recurso a la API Gmail: %s' % error)
        

def remove_permission(service, file_id, permission_id):
    '''
    Cambia el permiso de un archivo por el definido en el atributo permission_id.
    Args:
      service (Resource Drive): 
      file_id (str): id del archivo compartido
      permission_id (str): id del nuevo permiso
    '''
    try:
        service.permissions().delete(
            fileId=file_id, permissionId=permission_id).execute()
    except HttpError as error:
        print ('Ocurrio un error en el cambio de permiso de archivo: %s' % error)
