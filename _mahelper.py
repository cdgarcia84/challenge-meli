from email.mime.text import MIMEText
from googleapiclient.errors import HttpError

import base64


def message(sender, to, subject, message_text):
  '''
  Devuelve un diccionario con la clave raw como el mensaje del correo electronico.
  Este mensaje es un objeto MIMEText codificado en utf-8, convertido en base64.
  Dentro contiene la informacion definida por los argumentos.
  Args:
    sender (str): mail de quien envia el correo
    to (str): mail destino del correo
    subject (str): asunto del correo
    message_text (str): contenido del cuerpo del correo
  '''  
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw' : base64.urlsafe_b64encode(message.as_string().encode('utf-8')).decode('ascii')}


def send_message(service, user_id, message):
  '''
  Envia un correo desde la cuenta de user_id con los datos obtenido en message.
  Args:
    service (Resorce Gmail): Recurso a la API de Gmail. Este nos permitira enviar mails desde Gmail.
    user_id (str): direccion de mail del usuario que permitio su acceso a google drive
    message (str): mensaje de tipo MIMEText codificado en base64 que contenga la informacion 
                      necesaria para enviar un correo (to, from, subject, message_text)
  '''
  try:
    message = (service.users().messages().send(userId=user_id, body=message).execute())
    print ('Mail enviado: Id %s' % message['id'])
  except HttpError as error:
    print ('Ocurrio un error enviando el correo: %s' % error) 
