import socket

host = "localhost"
puerto = 5000

cliente = socket.socket();

cliente.connect((host, puerto));

for i in range(3):
    mensajes = "Mensaje " + str(i);
    cliente.send(mensajes.encode());

    respuesta = cliente.recv(1024).decode();
    print("Respuesta del servidor: ", respuesta)

cliente.send("FIN".encode());

respuesta_final = cliente.recv(1024).decode()
print(respuesta_final)

cliente.close();
