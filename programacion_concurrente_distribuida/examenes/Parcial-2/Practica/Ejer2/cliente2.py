import socket

host = "localhost"
puerto = 5000

cliente = socket.socket();

cliente.connect((host, puerto));

mensaje = "Peru es Clave";
cliente.send(mensaje.encode());

respuesta = cliente.recv(1024).decode();
print("Mensaje del servidor: ", respuesta);

cliente.close();