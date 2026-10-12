from flask import Flask, request, jsonify, render_template_string
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
DB_NAME = "tareas.db"

def iniciar_db():
    """creamos la db y las tablas"""
    conex = sqlite3.connect(DB_NAME)
    cursor = conex.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL)''')
    conex.commit()
    conex.close()

#Inicio del registro de usuarios
@app.route('/registro', methods=['POST'])
def registro():
    datos = request.get_json()
    if (not datos or 'usuario' 
        not in datos or 'contraseña'
        not in datos
    ):
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    nombre_usuario = datos['usuario']
    pass_plana = datos['contraseña']

    #hash de la pass
    hash_pass = generate_password_hash(pass_plana)
    conex = sqlite3.connect(DB_NAME)

    try:
        cursor = conex.cursor()
        cursor.execute(
            "INSERT INTO usuarios (usuario, password_hash) VALUES (?, ?)", #SE PONEN ? PARA EVITAR LA INYECCION 
            (nombre_usuario, hash_pass)    
        )
        conex.commit()
        return jsonify({"mensaje": f"Usuario '{nombre_usuario}' se registro correctamente"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "El usuario ya existe"}), 409
    except Exception as e:
        return jsonify({"error": f"Error del servidor: {str(e)}"}), 500
    finally:
        conex.close()

#Inicio de sesion de usuarios
@app.route('/login', methods=['POST'])
def login():
    datos = request.get_json()
    if (not datos or 'usuario'
        not in datos or 'contraseña'
        not in datos
    ):
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    nombre_usuario = datos['usuario']
    pass_plana = datos['contraseña']

    conex = sqlite3.connect(DB_NAME)
    cursor = conex.cursor()
    #Consulta parametrizada para buscar las credenciales (se usa ? para evitar inyeccion SQL)
    cursor.execute("SELECT password_hash FROM usuarios WHERE usuario = ?", (nombre_usuario,))
    resultado = cursor.fetchone()
    conex.close()

    #Comprobacion segura del hash almacenado
    if resultado and check_password_hash(resultado[0], pass_plana):
        return jsonify({"mensaje": f"Iniciaste sesion correctamente."}), 200
    else:
        return jsonify({"error": f"Revisa los datos ingresados"}), 401


#GET TAREAS

@app.route('/tareas', methods =['GET'])
def tareas():
    html_bienvenida = """
            <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Gestión de Tareas</title>
    </head>
    <body>
        <h1>Hola!! Ingresaste al Sistema de Gestión de Tareas!</h1>
        <p>Has iniciado sesión y accedido correctamente a la vista de tareas.</p>
    </body>
    </html>
    """
    return render_template_string(html_bienvenida)

#INICIAMOS LA BASE DE DATOS Y LEVANTOAMOS EL SV FLASK EN EL PUERTO 5000
if __name__ == '__main__':
    iniciar_db()
    app.run(port=5000, debug= True)