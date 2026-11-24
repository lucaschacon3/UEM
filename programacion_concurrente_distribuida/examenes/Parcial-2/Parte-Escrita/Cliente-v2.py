#PARTE ESCRITA
# Escribe un programa que cuente números, de uno en uno, en un servidor.
# El programa tendrá un cliente en un subproceso (cliente) que se comunicará 
# con el servidor mediante sockets.
# El cliente enviará una cierta cantidad de números aleatorios. Tras cada envío, 
# recibirá un OK cuando el servidor haya sumado el número.
# Cuando termine de enviar todos los números, enviará un mensaje FIN, cerrará la conexión y finalizará.
# Cuando el servidor reciba el mensaje FIN, también cerrará la conexión y finalizará.

import socket
import random

ip = "127.0.0.1"
port = 1234

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client_socket.connect((ip,port))


for i in range(10):
    numeros = random.randint(1,9)
    print(f"Enviamos => {numeros}")

    client_socket.sendall((str(numeros) + "\n").encode())

    data = client_socket.recv(1024)
    print(f"{data.decode()}")


client_socket.sendall(b"FIN\n")
print("Finalizando cliente => FIN")
client_socket.close()
