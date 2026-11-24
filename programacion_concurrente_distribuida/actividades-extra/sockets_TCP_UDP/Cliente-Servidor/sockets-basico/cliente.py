import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

mensaje = input("Mensaje: ")
client_socket.sendto(mensaje.encode(), ("127.0.0.1", 12345))

data, server_address = client_socket.recvfrom(1024)
print("Respuesta del servidor:", data.decode())

client_socket.close()
