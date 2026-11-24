#CLIENTE
#IMPORTAMOS SOCKET Q PERMITE COMUNICARSE CON LA RED
import socket

#IP CLIENTE Y SERVIDOR MISMO PC 
server_ip = "127.0.0.1"
#PUERTO DONDE ESCUCHA EL SERVIDOR 
server_port = 12345

#CREAMOS EL SOCKETS DEL CLIENTE 
#socket.socket => CREA UN SOCKET
# socket.AF_INET => usa  IPv4
# socket.SOCK_DGRAM PARA UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#PIDE AL USUARIO QUE ESCRIBA UN MENSAJE DESDE TECLADO CON INPUT
message = input("Escribe un mensaje para el servidor:")
#ENVIA MENSAJE AL SERVIDOR
#sendto =>ENVIA MENSAJE AL SERVIDOR METODO TIPICO DE UDP
#message.encode() => CONVIERTE EL MENSAJE A BYTES
# (server_ip, server_port) => DIRECCION DEL SERVIDOR 
client_socket.sendto(message.encode(), (server_ip, server_port))
#CIERRA EL SOCKET DEL CLIENTE
client_socket.close()
# Aunque en UDP no hay conexión real, siempre se cierra el socket.