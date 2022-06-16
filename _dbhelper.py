import mysql.connector


def connection(host, user, password, database=''):
    '''
    Retorna una coneccion activa a la base de datos
    Args:
      host (str): nombre o ip donde se ejecuta el servidor mysql
      user (str): nombre del usuario con permisos suficientes para trabajar la base de datos
      password (str): contrasenia del argumento user
      database (str): nombre de la base de datos. Por defecto su valor es ''    
    '''
    return mysql.connector.connect(host=host, user=user, password=password, database=database)


def createDatabase(conn, db):
    '''
    Crea una base de datos en caso de no existir previamente.
    Args:
      conn (MySQLConnection): conexion al motor donde se creara la base de datos en cuestion.
      db (str): nombre de la base de datos
    '''
    try:
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS " + db)
    except mysql.connector.errors.DatabaseError as errors:
        print(errors)
    finally:
        cursor.close()


def createTables(conn):
    '''
    Crea las tablas archivos y archivospublicos. Ambas tablas tiene las siguientes columnas.
      idArchivo, nobmreArchivo, extension, owner, esCompartido, fechaModificacion
    Como idArchivo como PRIMARY KEY
    
    Args:
      conn (MySQLConnection): conexion al motor donde se creara la base de datos en cuestion.
    '''
    try:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS archivos (idArchivo VARCHAR(255), nombreArchivo VARCHAR(255), extension VARCHAR(255), owner VARCHAR(255), esCompartido VARCHAR(255), fechaModificacion VARCHAR(255), PRIMARY KEY(idArchivo))")
        
        cursor.execute("CREATE TABLE IF NOT EXISTS archivospublicos (idArchivo VARCHAR(255), nombreArchivo VARCHAR(255), extension VARCHAR(255), owner VARCHAR(255), fechaModificacion VARCHAR(255), PRIMARY KEY(idArchivo))")
    except mysql.connector.errors.ProgrammingError as error:
        print('Ocurrio un error al crear las tablas archivos y/o archivospublicos: %s' % error)
    finally:
        cursor.close()

                                             
def insertFile(conn, items):
    '''
    Inserta un registro nuevo en la tabla archivo, si ya existe, lo actualiza.
    Args:
      conn (MySQLConnection): conexion al motor donde se creara la base de datos en cuestion.
      items (Array): cada item esta formado por id, name, extension, owner, esCompartido, fechaModificacion , todos formatos str
    '''
    try:        
        cursor = conn.cursor()

        for item in items:
            item["id"]
            item["name"]
            item["mimeType"]
            item['owners'][0]['emailAddress']
            item["shared"]
            item["modifiedTime"]
            cursor.execute(""" INSERT INTO archivos (idArchivo, nombreArchivo, extension, owner, esCompartido, fechaModificacion) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE nombreArchivo=%s, extension=%s, owner=%s, esCompartido=%s, fechaModificacion=%s""", (item["id"],item["name"],item["mimeType"],item['owners'][0]['emailAddress'],item["shared"],item["modifiedTime"],item["name"],item["mimeType"],item['owners'][0]['emailAddress'],item["shared"],item["modifiedTime"]))
            conn.commit()
            print("Se inserto un registro correctamente en la tabla archivos.")

    except mysql.connector.Error as error:
            print('Fallo el insert en la tabla archivos: %s' % error)
    finally:
        cursor.close()


def insertFilePublic(conn, id, name, mime_type, owners, modified_time):
    '''
    Inserta un registro nuevo en la tabla archivospublicos, si ya existe, lo actualiza.
    Args:
      conn (MySQLConnection): conexion al motor donde se creara la base de datos en cuestion.
      id (str): id del archivo
      name (str): nombre del archivo
      mime_type (str): extension del archivo
      owners (str): propietario del archivo
      modified_time (str): ultima fecha de modificacion
    '''
    try:        
        cursor = conn.cursor()
        mySql_insert_query = """INSERT INTO archivospublicos (idArchivo, nombreArchivo, extension, owner, fechaModificacion) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE nombreArchivo=%s, extension=%s, owner=%s, fechaModificacion=%s""" 

        recordTuple = (id, name, mime_type, owners, modified_time, name, mime_type, owners, modified_time)
        cursor.execute(mySql_insert_query, recordTuple)
        conn.commit()
        print("Se inserto un registro correctamente en la tabla archivospublicos.")

    except mysql.connector.Error as error:
        print('Fallo el insert en la tabla archivospublicos: %s' % error)
    finally:
        cursor.close()


def close(conn):
    '''
    Cierra la conexion con el motor de la base de datos.
    Args:
      conn (MySQLConnection): conexion al motor donde se creara la base de datos en cuestion.
    '''    
    if (conn.is_connected()):
        conn.close()
        print("Se cerro la conexion a MySQL.")
