import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("127.0.0.1", 12345))

print("Servidor escuchando en 127.0.0.1:12345")

while True:
    data, client_address = server_socket.recvfrom(1024)

    print(f"\nMensaje del cliente {client_address}: {data.decode()}")

    respuesta = input("Respuesta del servidor: ")
    
    server_socket.sendto(respuesta.encode(), client_address)
