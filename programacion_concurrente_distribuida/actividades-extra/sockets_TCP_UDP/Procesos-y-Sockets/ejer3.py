import socket
import threading
import random
import time

# Configuración del restaurante
CAPACIDAD = 9  # num máximo de mesas disponibles
mesas_ocupadas = 0
lock = threading.Lock()

# Función para manejar cada cliente
def manejar_cliente(conn, addr):
    global mesas_ocupadas
    print("Cliente conectado desde:", addr)
    continuar = True

    while continuar:
        # recibe mensaje del cliente
        mensaje = conn.recv(1024).decode()
        if mensaje:
            if mensaje == "SOLICITAR_MESA":
                lock.acquire()
                if mesas_ocupadas < CAPACIDAD:
                    mesas_ocupadas += 1
                    conn.sendall("MESA_ASIGNADA".encode())
                    print("Mesa asignada a", addr, "Mesas ocupadas:", mesas_ocupadas, "/", CAPACIDAD)
                else:
                    conn.sendall("NO_HAY_MESAS".encode())
                    print("No hay mesas disponibles para", addr)
                lock.release()

            elif mensaje == "LIBERAR_MESA":
                lock.acquire()
                if mesas_ocupadas > 0:
                    mesas_ocupadas -= 1
                    conn.sendall("MESA_LIBERADA".encode())
                    print("Mesa liberada por", addr, "Mesas ocupadas:", mesas_ocupadas, "/", CAPACIDAD)
                else:
                    conn.sendall("ERROR_LIBERAR".encode())
                lock.release()

            elif mensaje == "SALIR":
                print("Cliente", addr, "se desconecta.")
                continuar = False

    conn.close()

# Función principal del servidor
def servidor():
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.bind(("localhost", 12345))
    servidor_socket.listen(5)
    print("El restaurante está abierto y esperando clientes...")

    hilos = []  # lista para almacenar los hilos

    try:
        while True:
            conn, addr = servidor_socket.accept()
            hilo_cliente = threading.Thread(target=manejar_cliente, args=(conn, addr))
            hilo_cliente.start()
            hilos.append(hilo_cliente)  # agrega el hilo a la lista

    except KeyboardInterrupt:
        print("El restaurante está cerrando.")
    finally:
        # sspera a que todos los hilos terminen antes de cerrar el servidor
        for hilo in hilos:
            hilo.join()

        servidor_socket.close()

# Función para simular un cliente
def cliente():
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect(("localhost", 12345))

    # solicita una mesa
    cliente_socket.sendall("SOLICITAR_MESA".encode())
    respuesta = cliente_socket.recv(1024).decode()
    print("Respuesta del servidor:", respuesta)

    if respuesta == "MESA_ASIGNADA":
        # simula tiempo comiendo
        time.sleep(random.randint(1, 5))

        # libera la mesa
        cliente_socket.sendall("LIBERAR_MESA".encode())
        respuesta = cliente_socket.recv(1024).decode()
        print("Respuesta del servidor:", respuesta)

    # sale del restaurante
    cliente_socket.sendall("SALIR".encode())
    cliente_socket.close()

# ejecuta el servidor y varios clientes
if __name__ == "__main__":
    # ejecuta el servidor en un hilo separado 
    hilo_servidor = threading.Thread(target=servidor)
    hilo_servidor.start()

    # crea clientes aleatorios
    for _ in range(random.randint(10, 20)):
        threading.Thread(target=cliente).start()
        time.sleep(random.uniform(0.5, 2))

    # espera a que el servidor termine
    hilo_servidor.join()
