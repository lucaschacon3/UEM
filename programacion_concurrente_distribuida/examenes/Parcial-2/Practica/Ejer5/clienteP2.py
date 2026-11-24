
#CLIENTE PARCIAL 2 SOLO - PARTE ESCRITA EN DIGITAL

import socket
import random

host = "localhost"
puerto = 5000

cliente = socket.socket();
cliente.connect((host, puerto));

for i in range(5):
    numeros = random.randint(1, 10);
    cliente.send(str(numeros).encode());
    print("Numero enviado al Servidor: ", numeros)

    respuesta = cliente.recv(1024).decode();
    print("Respuesta del Servidor: ", respuesta)

cliente.send("FIN".encode());

cliente.close();
    