import socket

host = "localhost"
puerto = 5000

servidor = socket.socket();

servidor.bind((host, puerto));

servidor.listen(3);
print("Servidor Esperando conexion..")

conexion, direccion = servidor.accept();

bandera = True;
mensaje = conexion.recv(1024).decode();

while bandera:
    if mensaje == "FIN":
        bandera = False
        conexion.send("Conexion Cerrada".encode());
    else:
        print("Mensaje recibido: ", mensaje)
        respuesta = "Recibido: " + mensaje
        conexion.send(respuesta.encode())
        mensaje = conexion.recv(1024).decode();
        



conexion.close();
servidor.close();

