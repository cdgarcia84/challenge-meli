import os
import mysql.connector

class DataBase:

  # nombre de host donde se ejecuta la base de datos
  HOST = 'db-meli'
  # lee la varieble de entorno donde se almacena el valor correspondiente
  USER = os.getenv('MYSQL_USER')
  PASSWORD = open(os.getenv('MYSQL_PASSWORD_FILE'),'r').read().strip()
  DATABASE = os.getenv('MYSQL_DATABASE')

  def __init__(self, host=HOST, user=USER, password=PASSWORD, db=DATABASE):
    '''
    Inicializa la conexion a la base de datos en el parametro db. Ademas, crea las tablas archivos y archivospublicos.
    En caso de no existir la base de datos, la crea.
    Args:
      host (str): nombre o ip donde se ejecuta el servidor mysql. valor por defecto obtenido de una variable de 
                  entorno definida en la creacion del ambiente.
      user (str): nombre del usuario con permisos suficientes para trabajar la base de datos. valor por defecto
                  obtenido de una variable de entorno definida en la creacion del ambiente.
      password (str): contrasenia del argumento user. valor por defecto obtenido de una variable de entorno definida
                  en la creacion del ambiente.
      db (str): nombre de la base de datos. valor por defecto obtenido de una variable de entorno definida en la creacion del ambiente.      
    '''
    self.host = host
    self.user = user
    self.password = password
    self.db = db
    
    try:
      self.conn = mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.db)
    except mysql.connector.errors.ProgrammingError as error:
      self.conn = mysql.connector.connect(host=self.host, user=self.user, password=self.password, database="")
      
      # Crea una base de datos en caso de no existir previamente.
      try:
        cursor = self.conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS " + db)
      except mysql.connector.errors.DatabaseError as errors:
          print('Ocurrio un error al crear la base de datos: %s' % errors)
      finally:
          cursor.close()
          
      self.conn.close()
      self.conn = mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.db)
        
    self._createTables()

  def _createTables(self):
      '''
      Crea las tablas archivos y archivospublicos. Ambas tablas tiene las siguientes columnas.
        idArchivo, nobmreArchivo, extension, owner, esCompartido, fechaModificacion
      Como idArchivo como PRIMARY KEY      
      '''
      try:
          cursor = self.conn.cursor()
          cursor.execute("CREATE TABLE IF NOT EXISTS archivos (idArchivo VARCHAR(255), nombreArchivo VARCHAR(255), extension VARCHAR(255), owner VARCHAR(255), esCompartido VARCHAR(255), fechaModificacion VARCHAR(255), PRIMARY KEY(idArchivo))")
          
          cursor.execute("CREATE TABLE IF NOT EXISTS archivospublicos (idArchivo VARCHAR(255), nombreArchivo VARCHAR(255), extension VARCHAR(255), owner VARCHAR(255), fechaModificacion VARCHAR(255), PRIMARY KEY(idArchivo))")
      except mysql.connector.errors.ProgrammingError as error:
          print('Ocurrio un error al crear las tablas archivos y/o archivospublicos: %s' % error)
      finally:
          cursor.close()
                                             
  def insertFile(self, items):
      '''
      Inserta un registro nuevo en la tabla archivo, si ya existe, lo actualiza.
      Args:        
        items (Array): cada item esta formado por id, name, extension, owner, esCompartido, fechaModificacion , todos formatos str
      '''
      try:        
          cursor = self.conn.cursor()
          for item in items:
              item["id"]
              item["name"]
              item["mimeType"]
              item['owners'][0]['emailAddress']
              item["shared"]
              item["modifiedTime"]
              cursor.execute(""" INSERT INTO archivos (idArchivo, nombreArchivo, extension, owner, esCompartido, fechaModificacion) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE nombreArchivo=%s, extension=%s, owner=%s, esCompartido=%s, fechaModificacion=%s""", (item["id"],item["name"],item["mimeType"],item['owners'][0]['emailAddress'],item["shared"],item["modifiedTime"],item["name"],item["mimeType"],item['owners'][0]['emailAddress'],item["shared"],item["modifiedTime"]))
              self.conn.commit()
      except mysql.connector.Error as error:
          print('Fallo el insert en la tabla archivos: %s' % error)
      finally:
          cursor.close()

  def insertFilePublic(self, id, name, mime_type, owners, modified_time):
      '''
      Inserta un registro nuevo en la tabla archivospublicos, si ya existe, lo actualiza.
      Args:
        id (str): id del archivo
        name (str): nombre del archivo
        mime_type (str): extension del archivo
        owners (str): propietario del archivo
        modified_time (str): ultima fecha de modificacion
      '''
      try:        
          cursor = self.conn.cursor()
          mySql_insert_query = """INSERT INTO archivospublicos (idArchivo, nombreArchivo, extension, owner, fechaModificacion) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE nombreArchivo=%s, extension=%s, owner=%s, fechaModificacion=%s""" 

          recordTuple = (id, name, mime_type, owners, modified_time, name, mime_type, owners, modified_time)
          cursor.execute(mySql_insert_query, recordTuple)
          self.conn.commit()
      except mysql.connector.Error as error:
          print('Fallo el insert en la tabla archivospublicos: %s' % error)
      finally:
          cursor.close()

  def close(self):
      '''
      Cierra la conexion con el motor de la base de datos.
      '''    
      if (self.conn.is_connected()):
          self.conn.close()

  def check(self):
    try:
      cursor = self.conn.cursor(buffered=True)

      cursor.execute("SHOW COLUMNS FROM archivos")
      columns_arch = []
      for col in cursor.fetchall():
          columns_arch.append(col[0])

      cursor.execute("SELECT * FROM archivos")
      archivos = cursor.fetchall()

      cursor.execute("SHOW COLUMNS FROM archivospublicos")
      columns_archpub = []
      for col in cursor.fetchall():
          columns_archpub.append(col[0])

      cursor.execute("SELECT * FROM archivospublicos")
      archivospublicos = cursor.fetchall()

      return {'col_arch': columns_arch, 'arch': archivos, 'col_archpub': columns_archpub, 'archpub': archivospublicos}
    except mysql.connector.Error as error:
      print('Fallo el select en la tabla archivos y/o archivospublicos: %s' % error)
      return {}
    finally:
      cursor.close()
