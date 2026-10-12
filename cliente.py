import requests

URL_BASE = 'http://127.0.0.1:5000'


def registrar_user():
    print("/n--- Registro de Usuario ---")
    user= input("Ingresa tu nombre de usuario:")
    pass= input("Ingresa tu contrase;a").strip()
