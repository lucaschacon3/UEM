#PARTE ESCRITA
# Escribe un programa que cuente números, de uno en uno, en un servidor.
# El programa tendrá un cliente en un subproceso (cliente) que se comunicará 
# con el servidor mediante sockets.
# El cliente enviará una cierta cantidad de números aleatorios. Tras cada envío, 
# recibirá un OK cuando el servidor haya sumado el número.
# Cuando termine de enviar todos los números, enviará un mensaje FIN, cerrará la conexión y finalizará.
# Cuando el servidor reciba el mensaje FIN, también cerrará la conexión y finalizará.

import socket
import threading
import random

server_ip ="127.0.0.1"
server_port = 1234

def cliente ():

    cliente_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    cliente_socket.connect((server_ip,server_port))

    flag = True

    for i in range(10):

        numeros = random.randint(1,9)

        print(f"numeros => {numeros}")
        cliente_socket.send((str(numeros) + "\n").encode())

        data = cliente_socket.recv(1024)
        print(f"Mensaje recibido : {data.decode()}")

    cliente_socket.send(b"FIN\n")
    print("Enviamos FIN....")

h1 = threading.Thread(target=cliente)

h1.start()
h1.join()
