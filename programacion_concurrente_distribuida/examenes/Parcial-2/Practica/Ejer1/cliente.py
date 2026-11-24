import socket

cliente = socket.socket();

cliente.connect(("localhost", 5000));

mensaje = "Hola q haceee";
cliente.send(mensaje.encode());

respuesta = cliente.recv(1024).decode();
print("Respuesta del servidor:", respuesta)

cliente.close();
print("Conexión cerrada")
