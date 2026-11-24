import socket

host = "localhost"
puerto = 5000

servidor = socket.socket();

servidor.bind((host, puerto));

servidor.listen(1);
print("Servidor esperando conexión...")

conexion, direccion = servidor.accept();

numero = int (conexion.recv(1024).decode());
print("Número recibido:", numero)

if(numero >= 1 and numero <= 33):
    conexion.send("Numero Bajo".encode());
elif(numero >= 34 and numero <= 66 ):
    conexion.send("Numero Medio".encode());
else:
    conexion.send("Numero Alto".encode());

conexion.close()
servidor.close()
