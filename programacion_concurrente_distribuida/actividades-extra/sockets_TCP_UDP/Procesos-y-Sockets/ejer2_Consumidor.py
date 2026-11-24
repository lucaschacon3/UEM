import socket
import random
import time
import threading

# Cliente que envía peticiones
def consumidor(ip_servidor, puerto_servidor, ip_cliente, puerto_cliente, num_peticiones):
    # Crea el socket del cliente
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cliente_socket.bind((ip_cliente, puerto_cliente))

    # Archivo para registrar los pedidos
    archivo_pedidos = ip_cliente + "_" + str(puerto_cliente) + "_pedidos.txt"
    archivo_respuestas = ip_cliente + "_" + str(puerto_cliente) + "_respuestas.txt"

    # Registra los pedidos
    f_pedidos = open(archivo_pedidos, 'a')
    for _ in range(num_peticiones):
        tipo_pedido = random.choice(['A', 'B', 'C', 'D'])
        f_pedidos.write("Pedido: " + tipo_pedido + "\n")
        print("Enviando solicitud: " + tipo_pedido)
        cliente_socket.sendto(tipo_pedido.encode(), (ip_servidor, puerto_servidor))

        # Espera la respuesta del servidor
        respuesta, _ = cliente_socket.recvfrom(1024)
        respuesta = respuesta.decode()

        # Registra la respuesta
        f_respuestas = open(archivo_respuestas, 'a')
        f_respuestas.write("Respuesta: " + respuesta + "\n")
        f_respuestas.close()

        time.sleep(random.randint(1, 3))  # Simula el tiempo entre peticiones

    f_pedidos.close()

# Función para crear varios consumidores
def iniciar_consumidores(ip_servidor, puerto_servidor, num_consumidores, num_peticiones):
    consumidores = []
    for i in range(num_consumidores):
        ip_cliente = "127.0.0." + str(i+2)
        puerto_cliente = random.randint(10000, 20000)
        consumidor_thread = threading.Thread(target=consumidor, args=(ip_servidor, puerto_servidor, ip_cliente, puerto_cliente, num_peticiones))
        consumidores.append(consumidor_thread)
        consumidor_thread.start()

    for consumidor_thread in consumidores:
        consumidor_thread.join()

if __name__ == "__main__":
    ip_servidor = "127.0.0.1"
    puerto_servidor = 12345
    num_consumidores = 5  # num de clientes consumidores
    num_peticiones = 10  # num de peticiones por consumidor

    # Inicia los consumidores
    iniciar_consumidores(ip_servidor, puerto_servidor, num_consumidores, num_peticiones)
