import socket
import random
import time
import threading
import queue

# Cola de productos
cola = queue.Queue()

# Genera productos aleatorios
def generar_producto():
    # Genera un producto con características aleatorias
    producto = {
        'tipo': random.choice(['A', 'B', 'C', 'D']),
        'valor': random.randint(1, 100)
    }
    return producto

# Servidor que produce productos y los pone en la cola
def productor():
    while True:
        producto = generar_producto()
        cola.put(producto)
        print("Producto generado: " + str(producto))
        time.sleep(random.randint(1, 3))  # simula el tiempo de producción

# Servidor que maneja las peticiones de los consumidores
def servidor():
    # Dirección del servidor
    servidor_ip = "127.0.0.1"
    puerto = 12345
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor_socket.bind((servidor_ip, puerto))
    print("Servidor escuchando en " + servidor_ip + ":" + str(puerto))

    while True:
        # Recibe la solicitud del consumidor
        mensaje, direccion_cliente = servidor_socket.recvfrom(1024)
        tipo_pedido = mensaje.decode()
        print("Solicitud recibida de " + str(direccion_cliente) + ": " + tipo_pedido)

        # Verifica si hay productos en la cola
        if not cola.empty():
            producto = cola.get()
            if producto['tipo'] == tipo_pedido:
                # si el producto cumple con el criterio, lo entrega
                respuesta = "Producto entregado: " + str(producto)
                servidor_socket.sendto(respuesta.encode(), direccion_cliente)
                print("Producto entregado a " + str(direccion_cliente) + ": " + str(producto))
            else:
                # si no cumple, lo reincorpora a la cola
                cola.put(producto)
                respuesta = "Producto no disponible"
                servidor_socket.sendto(respuesta.encode(), direccion_cliente)
                print("Producto no disponible para " + str(direccion_cliente))
        else:
            respuesta = "No hay productos disponibles"
            servidor_socket.sendto(respuesta.encode(), direccion_cliente)
            print("No hay productos disponibles para " + str(direccion_cliente))

# Inicia el productor y servidor
def iniciar_servidor():
    # inicia el productor en un hilo
    threading.Thread(target=productor, daemon=True).start()
    
    # inicia el servidor en el hilo principal
    servidor()

if __name__ == "__main__":
    iniciar_servidor()
