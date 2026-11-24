
#SERVIDOR PARCIAL 2 SOLO - PARTE ESCRITA EN DIGITAL

import socket

host = "localhost"
puerto = 5000

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((host, puerto));

servidor.listen(1);
print("Servidor esperando conexion..")

conexion, direccion = servidor.accept();

band = True;
suma = 0;
contador = 0;

while band : 
    mensaje = conexion.recv(1024).decode();
    if mensaje == "FIN":
        band = False;
        conexion.send("Finalizando..".encode());
        print("Cerrando servidor..")
    else :
        numeros = int (mensaje)
        suma += numeros
        contador += 1
        conexion.send("OK".encode());
        print("Numero Recibido del Cliente: ", numeros)

print("Suma Total: ", suma)
print("Cantidad de Numeros Recibidos: ", contador)

conexion.close();
servidor.close();