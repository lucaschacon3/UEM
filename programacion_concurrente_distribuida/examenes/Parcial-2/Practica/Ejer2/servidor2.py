import socket

host = "localhost"
puerto = 5000

servidor = socket.socket();

servidor.bind((host, puerto));

servidor.listen(1);
print("Servidor Esperando conexion..")

conexion, direccion = servidor.accept();

mensaje = conexion.recv(1024).decode();
print("El mensaje del cliente es: ", mensaje)

respuesta = "Mensaje recibido correctamente"
conexion.send(respuesta.encode());

conexion.send(mensaje.encode());

conexion.close();
servidor.close();


# Cosas Utilizadas
# socket.socket() → Crea un socket para comunicarse.
# bind() → Le dice dónde va a estar (localhost, puerto 5000).
# listen(1) → Espera una conexión.
# accept() → Acepta la primera conexión que llegue.
# recv() → Recibe datos del cliente.
# send() → Envía un mensaje de vuelta al cliente.
# close() → Cierra la conexión.