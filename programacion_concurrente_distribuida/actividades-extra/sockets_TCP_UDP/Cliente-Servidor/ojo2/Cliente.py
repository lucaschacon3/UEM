# CLIENTE
# Crear socket
# Importamos el módulo socket para trabajar con sockets de red.
import socket

def client():
    # Creamos un socket utilizando IPv4 (AF_INET) y el protocolo TCP (SOCK_STREAM).
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Definimos la dirección IP y el puerto del servidor al que nos conectaremos.
    host = '127.0.0.1'  # Dirección localhost
    port = 12345        # Puerto del servidor

    # Establecemos la conexión con el servidor.
    client_socket.connect((host, port))
    print("Conectado al servidor en {}:{}".format(host, port))

    activo = True  # Variable para controlar el ciclo de comunicación.
    while activo:
        # Solicitamos al usuario del cliente que escriba un mensaje para enviar al servidor.
        client_message = input("Cliente: ")
        # Enviamos el mensaje al servidor codificado en UTF-8.
        client_socket.send(client_message.encode('utf-8'))
        if client_message.lower() == 'salir':  # Si el cliente envía "salir", cerramos la comunicación.
            print("Cliente ha terminado la conversación.")
            activo = False
        else:
            # Recibimos una respuesta del servidor. El tamaño máximo del mensaje es de 1024 bytes.
            server_message = client_socket.recv(1024).decode('utf-8')
            if server_message.lower() == 'salir':  # Si el servidor envía "salir", cerramos la comunicación.
                print("Servidor ha terminado la conversación.")
                activo = False
            else:
                print("Servidor:", server_message)  # Mostramos el mensaje recibido.

    # Cerramos el socket del cliente al terminar la comunicación.
    client_socket.close()

# Punto de entrada del programa. Llamamos a la función del cliente si este archivo es ejecutado directamente.
if __name__ == "__main__":
    client()