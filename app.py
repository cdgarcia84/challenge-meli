import os

from googleapiclient.errors import HttpError

import _dbhelper
import _gghelper
import _mahelper

# nombre de host donde se ejecuta la base de datos
HOST = 'db-meli'
# lee la varieble de entorno donde se almacena el valor correspondiente
USER = os.getenv('MYSQL_USER')
PASSWORD = open(os.getenv('MYSQL_PASSWORD_FILE'),'r').read().strip()
DATABASE = os.getenv('MYSQL_DATABASE')

# crea la base de datos, en caso de no existir
_dbhelper.createDatabase(_dbhelper.connection(HOST, USER, PASSWORD), DATABASE)

# se conecta a la base de datos definida en DATABASE y crea las tablas archivos y archivospublicos
conn = _dbhelper.connection(HOST, USER, PASSWORD, DATABASE)
_dbhelper.createTables(conn)

# realiza las conexiones a los recursos de google
service_drive = _gghelper.drive()
service_gmail = _gghelper.gmail()

me = service_drive.about().get(fields="user/emailAddress").execute()["user"]["emailAddress"]

results = service_drive.files().list(
    fields="nextPageToken, files(name, id, mimeType, owners/emailAddress, owners/permissionId, shared, modifiedTime)").execute()

items = results.get('files', [])
for item in items :    
    idArchivo = item["id"]
    nombreArchivo = item["name"]
    extension = item["mimeType"]
    ownerId = item['owners'][0]['permissionId']
    ownerEmail = item['owners'][0]['emailAddress']
    shared = item["shared"]
    fechaModificacion = item["modifiedTime"]
    if shared == True :
        # inserta el archivo compartido para historial
        _dbhelper.insertFilePublic(conn, idArchivo, nombreArchivo, extension, ownerEmail, fechaModificacion)
        
        try:
            resultados = service_drive.permissions().list(fileId=idArchivo, fields="nextPageToken, permissions(id)").execute()
        except HttpError as error:
            print('Ocurrio un error al listar un archivo en drive: %s' % error)
            
        permisos = resultados.get('permissions', [])
        for permiso in permisos :
            idPermiso = permiso["id"]
            if idPermiso != ownerId :
                # quitar el permiso compartido
                _gghelper.remove_permission(service_drive,idArchivo,idPermiso)
                
                # genera el cuerpo del mail al owner del archivo
                mensaje = _mahelper.message(me, ownerEmail, 'Se convirtio a Privado un archivo suyo en Google Drive', nombreArchivo)
                
                # envia el mail notificando
                _mahelper.send_message(service_gmail, me, mensaje)

# se realiza el registro de los archivos listado en drive                
items = results.get('files', [])
_dbhelper.insertFile(conn, items)

# finaliza la coneccion a la base de datos
_dbhelper.close(conn)
