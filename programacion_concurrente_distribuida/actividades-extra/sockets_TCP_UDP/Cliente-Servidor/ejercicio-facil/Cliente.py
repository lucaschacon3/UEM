#Servidor TCP básico: servidor que escucha en localhost, 
# acepta una conexión, recibe un mensaje y lo muestra.
import socket

ip = "localhost"
port = 1234

cliente_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
cliente_socket.connect((ip,port))

flag = True

while flag:

    mensaje = input("Enviar mensaje :")
    cliente_socket.send(mensaje.encode())


    if mensaje != "exit":
        data = cliente_socket.recv(1024)
        print(f"Mensaje devuelto => {data.decode()}")
    else:
            flag = False

cliente_socket.close()