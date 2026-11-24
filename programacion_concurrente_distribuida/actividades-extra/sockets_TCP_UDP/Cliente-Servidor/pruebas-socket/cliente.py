import socket 

server_ip = "127.0.0.1"
server_port = 12345

client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
flag = True

while flag:

    mensaje = input("Enviar mensaje UDP : ")
    
    if mensaje == "exit":
        client_socket.sendto(mensaje.encode(),(server_ip,server_port))
        flag = False
    else:
        client_socket.sendto(mensaje.encode(),(server_ip,server_port))
        data,server_address = client_socket.recvfrom(1024)
        print(f"Mensaje recibido de {server_address} : {data.decode()}")

client_socket.close()
print("Cliente finalizado...")
