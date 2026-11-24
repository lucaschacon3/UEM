import socket
import random

host = "localhost"
puerto = 5000

cliente = socket.socket();

cliente.connect((host, puerto));

numero = random.randint(1,100);
print("Número enviado:", numero)

cliente.send(str(numero).encode());

respuesta = cliente.recv(1024).decode();
print("Respuesta del servidor: ", respuesta);

cliente.close();