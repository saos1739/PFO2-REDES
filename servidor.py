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
@app.rout('/registro', methods=['POST'])