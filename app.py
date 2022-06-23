from _dbhelper import DataBase
from _gghelper import Drive, Gmail

def prueba_db(db):
    print('\nVerificacion en la base de datos\n')
    print('Hostname: ' + db.HOST)
    print('Username: ' + db.USER)
    print('Password: ' + db.PASSWORD)
    print('Database: ' + db.DATABASE)
    print('Para establece una conexion directamente al motor:')
    print('\tmysql -h ' + db.HOST + ' -u ' + db.USER + ' -p\n')
    datos = db.check()

    print('Tabla archivo (SELECT * FROM archivos) :')
    print('-'*200)
    print(datos['col_arch'])
    print('-'*200)
    for arch in datos['arch']:
        print(arch)
    print('-'*200+'\n')

    print('Tabla archivopublico (SELECT * FROM archivopublico):')
    print('-'*200)
    print(datos['col_archpub'])
    print('-'*200)
    for arch in datos['archpub']:
        print(arch)
    print('-'*200)


if __name__ == "__main__":
    # realiza la conexion a la base de datos
    db = DataBase()

    # realiza las conexiones a los recursos de google
    service_drive = Drive()
    service_gmail = Gmail()    

    # se obtiene la lista de todos los archivo del drive
    items = service_drive.files().get('files', [])

    print("\n/////////////////////////////////////////////////////////////////////////////////////////////////////////////\n")
    print('Se ha accedido al Google Drive de ' + service_drive.me())
    print('Hay ' + str(len(items)) + ' archivos.')
    
    # se realiza el registro de los archivos en la base de datos
    db.insertFile(items)
    print('Los mismos ya fueron registrados en la base de datos y/o actualizados sus valores.\n')

    for item in items:
        print ('Archivo: ' + item["name"] + ' - ' + item["mimeType"] + ' con fecha de modificacion ' + item["modifiedTime"])
        if item["shared"] == True :                            
            permisos = service_drive.permissions(item["id"]).get('permissions', [])
            for permiso in permisos :
                idPermiso = permiso["id"]
                if idPermiso == "anyoneWithLink":
                    print('\tEste archivo es accesible para todos por medio un link.')
                    
                    # quitar el permiso compartido
                    service_drive.remove_permission(item["id"],idPermiso)
                    print('\tSe le revoco dicho permiso.')

                    # inserta el archivo compartido para historial
                    db.insertFilePublic(item["id"], item["name"], item["mimeType"], item['owners'][0]['emailAddress'], item["modifiedTime"])
                    print('\tSe guardo el registro en el historial de archivos compartidos.')
                    
                    # envia el mail notificando
                    service_gmail.send_message(service_drive.me(), item['owners'][0]['emailAddress'], item["name"])
                    print('\tSe envio un mail a ' + item['owners'][0]['emailAddress'] + ' indicando sobre el cambio efectuado.')
    #db.close()
    print('\nFin de la ejecucion.')

    print("\n/////////////////////////////////////////////////////////////////////////////////////////////////////////////\n")
    prueba_db(db)
    db.close()
    print("\n/////////////////////////////////////////////////////////////////////////////////////////////////////////////\n")
