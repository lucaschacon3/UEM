
#CLIENTE PARCIAL 2 SOLO - PARTE ESCRITA EN DIGITAL

import socket
import random

host = "localhost"
puerto = 5000
CANTIDAD_NUMEROS = random.randint(1,30);

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((host, puerto));

for i in range(CANTIDAD_NUMEROS):
    numeros = random.randint(1, 10);
    cliente.send(str(numeros).encode());
    print("Numero enviado al Servidor: ", numeros)

    respuesta = cliente.recv(1024).decode();
    print("Respuesta del Servidor: ", respuesta)

cliente.send("FIN".encode());

cliente.close();
    