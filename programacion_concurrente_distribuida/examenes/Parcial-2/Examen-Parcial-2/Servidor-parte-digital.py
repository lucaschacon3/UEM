import socket
import threading
import time
import random

# python Servidor_EXAM2_PARTE_DIGITAL.py

# Configuración del servidor
HOST = 'localhost'
PUERTO = 12345
MAXIMO = 50  # Valor máximo permitido en la suma total por cliente

sumas = []  # Lista donde cada cliente guardará su suma
cliente_id = 0  # Para asignar una posición única en la lista a cada cliente
ejecutando = True  # Control general del servidor

# Función que se ejecuta por cada cliente conectado
def manejar_cliente(conexion, direccion, id_cliente):
    conectado = True
    suma = 0

    while conectado:
        datos = conexion.recv(1024).decode()  # Recibir datos del cliente

        if datos == "FIN":
            # Si el cliente envía FIN, le mandamos la suma total y cerramos
            conexion.send(str(suma).encode())
            conectado = False
        else:
            try:
                numero = int(datos)
                suma += numero

                # Si el cliente se pasa del máximo permitido
                if suma >= MAXIMO:
                    conexion.send("MAX".encode())
                    # Luego de enviar MAX, esperamos el FIN y respondemos con la suma
                    datos = conexion.recv(1024).decode()
                    if datos == "FIN":
                        conexion.send(str(suma).encode())
                    conectado = False
                else:
                    # Si todo está bien, esperamos de 2 a 5 segundos y respondemos OK
                    time.sleep(random.randint(2, 5))
                    conexion.send("OK".encode())
            except ValueError:
                # Si lo que se recibe no es un número válido
                conexion.send("ERROR".encode())

    conexion.close()


# Crear socket y esperar conexiones
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PUERTO))
servidor.listen()

print("Servidor escuchando en el puerto", PUERTO)

while ejecutando:
    conexion, direccion = servidor.accept()
    print("Conexión aceptada de", direccion)

    # Asignar un ID único a cada cliente
    sumas.append(0)
    id_actual = cliente_id
    cliente_id += 1

    # Lanzar hilo para atender al cliente
    hilo = threading.Thread(target=manejar_cliente, args=(conexion, direccion, id_actual))
    hilo.start()
