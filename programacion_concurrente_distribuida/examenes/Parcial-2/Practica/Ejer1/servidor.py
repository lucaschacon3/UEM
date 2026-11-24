import socket

servidor = socket.socket();   

servidor.bind(("localhost", 5000));

servidor.listen(1);
print("Servidor Esperando conexion..")

conexion, direccion = servidor.accept();
print("Cliente conectado desde: ", direccion)

mensaje = conexion.recv(1024).decode();
print("Mensaje recibido del cliente:", mensaje)

respuesta = "Mensaje recibido";
conexion.send(respuesta.encode())

conexion.close();
print("Conexión cerrada")


# Cosas Utilizadas
# socket.socket() → Crea un socket para comunicarse.
# bind() → Le dice dónde va a estar (localhost, puerto 5000).
# listen(1) → Espera una conexión.
# accept() → Acepta la primera conexión que llegue.
# recv() → Recibe datos del cliente.
# send() → Envía un mensaje de vuelta al cliente.
# close() → Cierra la conexión.
# encode() -> para string sino hay q usar int(numero)
# decode() -> devuelve un string, si se quer un int se hace numero = int (conn.recv(1024).decode())