import socket

server_ip = "127.0.0.1"
server_port = 12345

servidor_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

servidor_socket.bind((server_ip,server_port))

print(f"Escuchando {server_ip},{server_port}")

flag = True

while flag:

    data,client_address =  servidor_socket.recvfrom(1024)
    print(f"Mensaje recibido de {client_address} : {data.decode()}")

    if data.decode() == "exit":
        flag = False
    else:
        mensaje = input("Enviar mensaje a client UDP :")
        servidor_socket.sendto(mensaje.encode(),(client_address))

servidor_socket.close()
print("Servidor finalizado...")