import socket  # Librería para comunicación por red usando sockets (aquí usas TCP)


def connectar(ip, port):
    # Crea y conecta un cliente TCP al servidor (ip, port)
    # Devuelve:
    #   client_socket -> el socket para enviar datos
    #   archivo       -> "archivo" para leer líneas con readline()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea socket TCP (IPv4 + TCP)

    client_socket.connect((ip, port))  # Conecta el cliente al servidor (si el servidor no está escuchando, falla)

    archivo = client_socket.makefile("r")  # Crea un "archivo" de lectura para poder hacer archivo.readline()

    return client_socket, archivo  # Devuelve ambos: el socket (para send) y el archivo (para recibir por líneas)


def enviar_linea(client_sock, text):
    # Envía un texto (o número) al servidor en formato "línea"
    # Importante: agrega "\n" al final para que el servidor pueda usar readline()

    client_sock.send((str(text) + "\n").encode())  # Convierte a string, añade salto de línea, pasa a bytes y envía


def recv_linea(archivo):
    # Lee una línea completa desde el servidor (hasta '\n')
    # Devuelve el texto limpio (sin '\n') o un valor si la conexión se cerró

    line = archivo.readline()  # Lee una línea del servidor (si no hay '\n', puede quedarse esperando)

    if not line:               # Si viene vacío, es que el servidor cerró la conexión
        return ""             # Devuelves un string " " (ojo: suele ser mejor "" o None)

    return line.strip()        # Devuelve la línea sin espacios ni '\n'
