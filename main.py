import base64
import json
from email.mime.image import MIMEImage

import qrcode
from PIL import Image
import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import psycopg2
import select
# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from flask import Flask, render_template, request, make_response, redirect
from jinja2 import Environment, FileSystemLoader
from ddbb import get_db_connection


# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


app = Flask(__name__)
conexion = None
tunnel = None

def generar_qr_base64(data):
    # Generar la imagen QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    # Guardar la imagen en un buffer y convertirla a base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    qr_image_base64 = base64.b64encode(buffer.getvalue()).decode()

    return qr_image_base64



def enviar_email(data):

    # Sustituye con tu dirección de correo
    remitente = "correoexpendable12@gmail.com"  # Dirección de correo del remitente
    # Sustituye con la dirección de correo del destinatario

    destinatario = data.get('email')  # Dirección de correo del destinatario
    # Cargar y renderizar la plantilla con Jinja2
    env = Environment(loader=FileSystemLoader('templates'))  # 'templates' es el directorio con tu plantilla HTML
    template = env.get_template('email_template.html')
    html_content = template.render(campoEmail=data.get('email'),
                                   codigo=data.get('codigo'))

    mensaje_email = MIMEMultipart()
    # Adjuntar el contenido HTML al mensaje
    mensaje_email.attach(MIMEText(html_content, "html"))

    #mensaje_email = MIMEText(mensaje)
    mensaje_email["Subject"] = "Notificación de actualización en ordenes"  # Asunto del correo
    mensaje_email["From"] = remitente
    mensaje_email["To"] = destinatario

    qr_base64 = generar_qr_base64(data.get('codigo'))  # Pasar aqui el codigo para convertirlo imagen qr
    # Incrustar el QR como una imagen inline
    img_data = base64.b64decode(qr_base64)
    image = MIMEImage(img_data, name="qr_code.png")
    image.add_header('Content-ID', '<qr_code>')  # Usar un ID único para referenciar en el HTML
    mensaje_email.attach(image)

    # Configuración del servidor SMTP
    try:
        # Usamos Gmail como ejemplo. Cambia si usas otro proveedor
        with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
            servidor.starttls()  # Establecer conexión segura
            # Cambia por tu contraseña de correo o contraseña de aplicación
            servidor.login(remitente, "iqba bejw tchr iblg")  # Contraseña o contraseña de aplicación
            servidor.sendmail(remitente, destinatario, mensaje_email.as_string())
            print("Correo enviado con éxito.")
    except Exception as e:
        print(f"Ocurrió un error al enviar el correo: {e}")


def enviar_pago(data):

    # Sustituye con tu dirección de correo
    remitente = "correoexpendable12@gmail.com"  # Dirección de correo del remitente
    # Sustituye con la dirección de correo del destinatario

    destinatario = data.get('email')  # Dirección de correo del destinatario
    # Cargar y renderizar la plantilla con Jinja2
    env = Environment(loader=FileSystemLoader('templates'))  # 'templates' es el directorio con tu plantilla HTML
    template = env.get_template('pago_template.html')
    html_content = template.render(campoEmail=data.get('email'),
                                   campoConcierto=data.get('concierto'),
                                   campoButaca = data.get('butaca'),
                                   campoPrecio = data.get('precio'))

    mensaje_email = MIMEMultipart()
    # Adjuntar el contenido HTML al mensaje
    mensaje_email.attach(MIMEText(html_content, "html"))

    #mensaje_email = MIMEText(mensaje)
    mensaje_email["Subject"] = "Notificación de actualización en ordenes"  # Asunto del correo
    mensaje_email["From"] = remitente
    mensaje_email["To"] = destinatario


    # Configuración del servidor SMTP
    try:
        # Usamos Gmail como ejemplo. Cambia si usas otro proveedor
        with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
            servidor.starttls()  # Establecer conexión segura
            # Cambia por tu contraseña de correo o contraseña de aplicación
            servidor.login(remitente, "iqba bejw tchr iblg")  # Contraseña o contraseña de aplicación
            servidor.sendmail(remitente, destinatario, mensaje_email.as_string())
            print("Correo enviado con éxito.")
    except Exception as e:
        print(f"Ocurrió un error al enviar el correo: {e}")






# with SSHTunnelForwarder(
#         ("mvs.sytes.net", 11080),  # Dirección y puerto del servidor SSH (usuario debe cambiar estos valores)
#         ssh_username="sshuser",  # Usuario SSH (usuario debe cambiar este valor)
#         ssh_pkey="C:\\Users\\hecto\\Desktop\\acceso remoto\\accesso remoto pve\\id_rsa",
#         # Ruta a tu archivo id_rsa (usuario debe proporcionar la ruta correcta)
#         # ssh_key_password="<TU_PASSPHRASE>",  # Passphrase para la clave privada (si la tiene)
#         remote_bind_address=("localhost", 5432),
#         # Dirección y puerto del servidor PostgreSQL (usuario debe cambiar estos valores)
#         local_bind_address=("localhost", 22)  # Puerto local para el túnel (puede cambiarse si es necesario)
# ) as tunnel:
#     print("Túnel SSH establecido con éxito.")  # Imprime un mensaje cuando el túnel SSH esté listo
#
#     # Conexión a la base de datos PostgreSQL a través del túnel SSH
conexion = psycopg2.connect(
    dbname="erictickets",  # Nombre de la base de datos (usuario debe proporcionar el nombre correcto)
    user="postgres",  # Usuario de la base de datos (usuario debe proporcionar el usuario adecuado)
    password="1234",  # Contraseña de la base de datos (usuario debe proporcionar la contraseña correcta)
    host="localhost",  # Usamos localhost porque estamos trabajando a través del túnel SSH
    port=5432  # Usar el puerto del túnel para la conexión local
)

# Establecer el nivel de aislamiento para la conexión
conexion.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conexion.cursor()

# Ejecutar un comando SQL para escuchar las notificaciones en el canal 'ventas_notificaciones'

cursor.execute("LISTEN registro_notificaciones;")
cursor.execute("LISTEN pago_notificaciones;")



print("Escuchando actualizaciones...")  # Indica que está escuchando las notificaciones

# Abrir el archivo de log de forma manual en modo 'a' (append) para agregar nuevas entradas
log_file = open('log_actualizaciones.txt', 'a')

try:
    while True:
        # Esperar notificación de cambios en la base de datos
        if select.select([conexion], [], [], 5) == ([], [], []):
            # Si no hay notificaciones, espera 5 segundos antes de continuar
            print("Esperando notificación...")
        else:
            conexion.poll()  # Verificar si hay nuevas notificaciones
            while conexion.notifies:
                # Si hay notificaciones, procesarlas
                notificacion = conexion.notifies.pop(0)

                data = json.loads(notificacion.payload)
                print(data)
                print("Notificación recibida:", notificacion.payload)  # Imprime la notificación en la consola

                # Escribir la notificación en el archivo de log
                log_file.write(f"Notificación recibida: {notificacion.payload}\n")
                log_file.flush()  # Asegúrate de que los datos se escriben inmediatamente en el archivo
            if notificacion.channel == "registro_notificaciones":
                enviar_email(data)
            if notificacion.channel == "pago_notificaciones":
                enviar_pago(data)


except KeyboardInterrupt:
    print("Cerrando la conexión...")  # Si se interrumpe el proceso, imprime este mensaje

finally:
         # Cerrar el cursor y la conexión de forma segura
    cursor.close()
    conexion.close()
    log_file.close()  # No olvides cerrar el archivo de log

# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     conexion, tunnel = get_db_connection()
#     app.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
