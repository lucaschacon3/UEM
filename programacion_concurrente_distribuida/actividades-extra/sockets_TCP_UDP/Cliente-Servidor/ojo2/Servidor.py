# Crear socket
# Importamos el módulo socket para trabajar con sockets de red.
import socket

def server():
    # Creamos un socket utilizando IPv4 (AF_INET) y el protocolo TCP (SOCK_STREAM).
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Definimos la dirección IP y el puerto donde el servidor escuchará.
    host = '127.0.0.1'  # Dirección localhost
    port = 12345        # Puerto para la conexión

    # Asociamos el socket al host y puerto definidos.
    server_socket.bind((host, port))

    # Configuramos el socket para escuchar conexiones entrantes, permitiendo una cola de 1 conexión.
    server_socket.listen(1)
    print("Esperando conexiones en {}:{}".format(host, port))

    # Aceptamos una conexión entrante. Esto devuelve un nuevo socket y la dirección del cliente.
    cliente, direccion = server_socket.accept()
    print("Conexión establecida con:", direccion)

    activo = True  # Variable para controlar el ciclo de comunicación.
    while activo:
        # Recibimos un mensaje del cliente. El tamaño máximo del mensaje es de 1024 bytes.
        cliente_message = cliente.recv(1024).decode('utf-8')
        if cliente_message.lower() == 'salir':  # Si el cliente envía "salir", cerramos la comunicación.
            print("Cliente ha terminado la conversación.")
            activo = False
        else:
            print("Cliente:", cliente_message)  # Mostramos el mensaje recibido.

        # Solicitamos al usuario del servidor que escriba una respuesta.
        server_message = input("Servidor: ")
        # Enviamos el mensaje al cliente codificado en UTF-8.
        cliente.send(server_message.encode('utf-8'))
        if server_message.lower() == 'salir':  # Si el servidor envía "salir", cerramos la comunicación.
            print("Servidor ha terminado la conversación.")
            activo = False

    # Cerramos los sockets del cliente y del servidor al terminar la comunicación.
    cliente.close()
    server_socket.close()

# Punto de entrada del programa. Llamamos a la función del servidor si este archivo es ejecutado directamente.
if __name__ == "__main__":
    server()

