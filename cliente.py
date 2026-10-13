import requests
URL_BASE = 'http://127.0.0.1:5000'

#registro de usuarios
def registrar_user():
    print("\n--- Registro de Usuario ---")
    user= input("Ingresa tu nombre de usuario: ").strip()
    password= input("Ingresa tu contraseña: ").strip()

    payload = {
    "usuario": user,
    "contraseña": password,
    }

    try:
        respuesta = requests.post(f"{URL_BASE}/registro", json=payload)
        datos = respuesta.json()
        print(f"[{respuesta.status_code}] {datos.get('mensaje', datos.get('error'))}")
    except Exception as e:
        print(f"Ocurrio un error al conectar con el servidor: {e}")

#pasarela de login
def iniciar_sesion():
    print("\n --- Inicio de Sesion---")
    user= input("Ingresa tu nombre de usuario: ").strip()
    password= input("Ingresa tu contraseña: ").strip()

    payload = {
    "usuario": user,
    "contraseña": password,
    }

    try:
        respuesta = requests.post(f"{URL_BASE}/login", json=payload)
        datos = respuesta.json()
        print(f"[{respuesta.status_code}]{datos.get('mensaje', datos.get('error'))}")

#login exitoso
        if respuesta.status_code == 200:
            ver_tareas()
    except Exception as e:
        print (f"Ocurrio un error al conectar con el servidor : {e}")


#acceso a tareas
def ver_tareas():
    print("\n --- Bienvenido a tus tareas---")
    try:
        respuesta = requests.get(f"{URL_BASE}/tareas")
        #verificamos el acceso con el code 200
        if respuesta.status_code == 200:
            #si nos da el code 200
            print("Acceso exitoso a la seccion de Tareas.")
        #caso de error
        else:
            print(f"no se pudo acceder a las tareas. Error {respuesta.status_code}")
    except Exception as e:
        print(f"Ocurrio un error al consultar las tareas: {e}")


#menu principal

def main_menu():
    while True:
        print(" Bienvenido al sistema de gestion de tareas!!")
        print("==============================")
        print("1. Registrarse ")
        print("2. Iniciar sesion ")
        print("3. Salir ")

        opcion = input("Elige tu opcion: 1, 2 o 3: ").strip()
        if opcion == "1":
            registrar_user()
        elif opcion == "2":
            iniciar_sesion()
        elif opcion == "3":
            print("Hasta la proxima!")
            break
        else:
            print("Opcion invalida. Reingresa tu opcion")

if __name__ == "__main__":
    main_menu()


