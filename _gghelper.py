import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from email.mime.text import MIMEText

import base64

class connAPI:    
    '''
    Retorna un recurso a la API de Google Drive. Este recurso nos permitira acceder a los archivos guardados
    en Drive. De esta manera se podra listarlos y cambiar los permisos de los mismo cuando fuera necesario.
    
    Utilizando las credenciales obtenidas para usar la API de Google Drive, almacenadas en credentials_drive.json
    genera un token por usuario, una vez que este acepta los permisos requeridos en el scope. Este token sera
    almacenado en token_drive.json
    El token sirve para que el usuario no tenga que aceptar los permisos cada vez que accede a la app.
    Si se quiere cambiar de usuario se debe borrar el archivo token_drive.json
    '''
    def conectionAPI(self):#scope, token, credentials, app, version):
        creds = None
        if os.path.exists(self.TOKEN):
            creds = Credentials.from_authorized_user_file(self.TOKEN, self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.CREDENCIAL, self.SCOPES)
                creds = flow.run_console()
            with open(self.TOKEN, 'w') as tokenn:
                tokenn.write(creds.to_json())
        try:
            service = build(self.API[0], self.API[1], credentials=creds)
            return service
        except HttpError as error:
            print('Ocurrio un error al generar el recurso a la API: %s' % error)
    

class Drive(connAPI):
    SCOPES = ['https://www.googleapis.com/auth/drive']
    TOKEN = 'token_drive.json'
    CREDENCIAL = 'credentials_drive.json'
    API = ['drive','v3']
    
    def __init__(self):
        '''
        Inicia la conexion a la api de drive.
        '''
        self.serv = self.conectionAPI()
        
    def me(self):
        '''
        Retorna la cuenta de correo del usuario que dio permisos de usar la api.
        '''
        return self.serv.about().get(fields="user/emailAddress").execute()["user"]["emailAddress"]
    
    def files(self):
        '''
        Retorna una lista de los archivos que se encuentran en el drive.
        '''
        return self.serv.files().list(fields="nextPageToken, files(name, id, mimeType, owners/emailAddress, owners/permissionId, shared, modifiedTime)").execute()
    
    def permissions(self, idArchivo):
        '''
        Retorna la lista de permisos asociado al archivo identificado por el parametro idArchivo. Retorna una lista vacia en caso de no poder obtenerlos.
        Args:
          idArchivo (str): id del archivo que se desea obtener la lista de permisos.
        '''
        try:
            resultados = self.serv.permissions().list(fileId=idArchivo).execute()
            return resultados
        except HttpError as error:
            print('Ocurrio un error al listar los permisos del archivo en drive: %s' % error)
            resultados = []
            return resultados            
            
    def remove_permission(self, file_id, permission_id):
        '''
        Cambia el permiso de un archivo por el definido en el atributo permission_id.
        Args:
        service (Resource Drive): 
        file_id (str): id del archivo compartido
        permission_id (str): id del nuevo permiso
        '''
        try:
            self.serv.permissions().delete(fileId=file_id, permissionId=permission_id).execute()
        except HttpError as error:
            print ('Ocurrio un error en el cambio de permiso de archivo: %s' % error)


class Gmail(connAPI):
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    TOKEN = 'token_gmail.json'
    CREDENCIAL = 'credentials_gmail.json'
    API = ['gmail','v1']
    
    def __init__(self):
        '''
        Inicia la conexion a la api de gmail
        '''
        self.serv = self.conectionAPI()

    def send_message(self, user_id, to, archivo):
        '''
        Envia un correo desde la cuenta de user_id a la cuenta establecida en to informando sobre la eliminacion
        de permisos de accesos publicos sobre el archivo definido en el parametro archivo.
        Args:
            user_id (str): direccion de mail del usuario que permitio su acceso a google drive
            to (str): mail destino del correo
            archivo (str): nombre del archivo al que se le cambio el permiso
        '''
        message = MIMEText('El archivo ' + archivo + ' dejo de ser accesible por medio de link.')
        message['to'] = to
        message['from'] = user_id
        message['subject'] = 'Se convirtio a Privado un archivo suyo en Google Drive'
        msj = {'raw' : base64.urlsafe_b64encode(message.as_string().encode('utf-8')).decode('ascii')}
        
        try:
            message = (self.serv.users().messages().send(userId=user_id, body=msj).execute())            
        except HttpError as error:
            print ('Ocurrio un error enviando el correo: %s' % error) 
