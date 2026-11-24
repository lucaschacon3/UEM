import socket

# python Cliente_EXAM2_PARTE_DIGITAL.py


# ==========================
# Capa de datos (conexión)
# ==========================
def conectar_servidor():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(('localhost', 12345))
    return cliente

def enviar(cliente, mensaje):
    cliente.send(str(mensaje).encode())

def recibir(cliente):
    return cliente.recv(1024).decode()

# ==========================
# Capa de negocio (lógica)
# ==========================
def manejar_cliente():
    cliente = conectar_servidor()
    terminado = False

    while not terminado:
        numero = input("Introduce un número o escribe FIN para terminar: ")

        if numero == "FIN":
            enviar(cliente, "FIN")
            respuesta = recibir(cliente)
            print("Suma total recibida:", respuesta)
            terminado = True
        else:
            enviar(cliente, numero)
            respuesta = recibir(cliente)

            if respuesta == "OK":
                print("Servidor aceptó el número.")
            elif respuesta == "MAX":
                print("¡Se alcanzó el valor máximo permitido!")
                # Enviamos FIN automáticamente y recibimos la suma final
                enviar(cliente, "FIN")
                respuesta = recibir(cliente)
                print("Suma total recibida:", respuesta)
                terminado = True
            elif respuesta == "ERROR":
                print("Dato inválido. Por favor, ingresa un número.")
    
    cliente.close()
    print("Conexión cerrada.")

# ==========================
# Capa de usuario (interfaz)
# ==========================
print("Cliente iniciado. Conectando al servidor...")
manejar_cliente()
