# This is a sample Python script.
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import psycopg2
import select
# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from flask import Flask, render_template, request, make_response, redirect, jsonify
from jinja2 import Environment, FileSystemLoader
from sshtunnel import SSHTunnelForwarder

from ddbb import get_db_connection
from dotenv import load_dotenv
import os
import jwt

app = Flask(__name__)
conexion = None
tunnel = None


# Press the green button in the gutter to run the script.
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/code_check')
def code_check():
    return render_template('code_check.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/read_qr')
def read_qr():
    return render_template('read_qr.html')

@app.route('/qr_ok')
def qr_ok():
    return render_template('qr_ok.html')

@app.route('/qr_fail')
def qr_fail():
    return render_template('qr_fail.html')


@app.route('/qr-data', methods=['POST'])
def qr_data():
    if request.is_json:
        qr_content = request.json.get('qr_data')
        print("Contenido del QR:", qr_content)

        # Responder con JSON indicando éxito y redirigir en el cliente
        return jsonify({"message": "QR recibido", "content": "qr_fail"})

    else:
        return jsonify({"error": "No se recibió JSON válido"}), 400





@app.route('/sign_in', methods=['POST'])
def sign_in():
    # Obtener los datos del formulario
    login = request.form['login']
    passwd = request.form['passwd']

    try:
        # Obtener un cursor de la conexión
        cursor = conexion.cursor()

        # Llamar al procedimiento almacenado 'login_usuario'
        cursor.callproc('login_usuario', (login, passwd))

        # Obtener el valor de retorno del procedimiento (booleano)
        result = cursor.fetchone()  # Debería devolver (True,) o (False,)
        if result and result[0]:
            print("Login exitoso.")
            # Generar un token JWT utilizando el nombre de usuario
            token = generate_token(login)  # deberemos usar generate_token(login) pero lo dejamos así de momento

            # Crear la respuesta
            response = make_response(redirect('/login_ok'))  # Redirigir a login_o

            # Establecer una cookie en la respuesta con el token JWT
            response.set_cookie('token', token)
            response.set_cookie('userlogin', login)

            # Devolver la respuesta con la cookie establecida
            return response

        else:
            print("Credenciales incorrectas.")
            return render_template("login_fail.html")

    except Exception as e:
        print(f"Error al llamar al procedimiento almacenado: {e}")
        return 'Error al verificar las credenciales.'

    finally:
        cursor.close()


@app.route('/register_in', methods=['POST'])
def register_in():
    # Obtener los datos del formulario
    user = request.form['user']
    email = request.form['email']
    phone = request.form['phone']
    address = request.form['address']
    passwd = request.form['passwd']

    try:
        # Obtener un cursor de la conexión
        cursor = conexion.cursor()

        # Llamar al procedimiento almacenado 'login_usuario'
        cursor.callproc('registrar_usuario', (user, email, phone, address, passwd))


        # Obtener el valor de retorno del procedimiento (booleano)
        result = cursor.fetchone()  # Debería devolver (True,) o (False,)
        conexion.commit()
        if result and result[0]:
            print("Registro exitoso.")

            return render_template('code_check.html')



        else:
            print("Credenciales incorrectas.")

    except Exception as e:
        print(f"Error al llamar al procedimiento almacenado: {e}")
        return 'Error al verificar las credenciales.'

    finally:
        cursor.close()


# Función para generar token
def generate_token(userlogin):
    # Codifica el token JWT con el nombre de usuario y la clave secreta
    token = jwt.encode({'userlogin': userlogin}, os.getenv('SECRET_KEY'), algorithm='HS512')
    return token


# Función para verificar token
def verify_token(token, userlogin):
    try:
        # Verifica la firma del token JWT utilizando la clave secreta
        decoded_token = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS512'])

        # Verificar si el nombre de usuario del token coincide con el usuario proporcionado
        if decoded_token['userlogin'] == userlogin:
            return True
    except jwt.ExpiredSignatureError:
        # Manejar el caso en que el token ha expirado
        return None
    except jwt.InvalidTokenError:
        # Manejar el caso en que el token es inválido
        return None


# Ejemplo de una ruta protegida
@app.route('/login_ok')
def login_ok():
    # Obtener el token y el nombre de usuario desde las cookies de la solicitud
    token = request.cookies.get('token')  # Obtener el token JWT de la cookie
    userlogin = request.cookies.get('userlogin')  # Obtener el nombre de usuario de la cookie

    # Verificar si el token o el nombre de usuario están ausentes
    if not token or not userlogin:
        # Si faltan el token o el nombre de usuario, renderizar una plantilla de error de token
        return render_template('token_fail.html')

    # Verificar la validez del token
    decoded_token = verify_token(token, userlogin)

    # Verificar si el token es válido
    if decoded_token:
        # Si el token es válido, renderizar la plantilla para la ruta protegida
        return render_template('login_ok.html')
    else:
        # Si el token no es válido, renderizar una plantilla de error de token
        return render_template('token_fail.html')




@app.route('/check_code', methods=['POST'])
def check_code():
    # Obtener los datos del formulario
    login = request.form['login']
    code = request.form['code']
    code = (int(code))
    try:
        # Obtener un cursor de la conexión
        cursor = conexion.cursor()

        # Llamar al procedimiento almacenado 'login_usuario'
        cursor.callproc('check_code', (login, code))

        # Obtener el valor de retorno del procedimiento (booleano)
        result = cursor.fetchone()  # Debería devolver (True,) o (False,)
        if result and result[0]:
            print("Login exitoso.")
            # Generar un token JWT utilizando el nombre de usuario
            token = generate_token(login)  # deberemos usar generate_token(login) pero lo dejamos así de momento

            # Crear la respuesta
            response = make_response(redirect('/login'))  # Redirigir a login_o

            # Establecer una cookie en la respuesta con el token JWT


            # Devolver la respuesta con la cookie establecida
            return response

        else:
            print("Credenciales incorrectas.")
            return render_template("login_fail.html")

    except Exception as e:
        print(f"Error al llamar al procedimiento almacenado: {e}")
        return 'Error al verificar las credenciales.'

    finally:
        cursor.close()



if __name__ == '__main__':
    conexion, tunnel = get_db_connection()
    app.run(ssl_context=('cert.pem', 'key.pem'), host='0.0.0.0', port=5000, debug=True);

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
