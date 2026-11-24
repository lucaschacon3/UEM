import socket

server_ip = "127.0.0.1"
server_port = 12345

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client_socket.connect((server_ip,server_port))

print(f"Conectado Client {server_ip},{server_port}")

flag = True

while flag:
    mensaje = input("Escribir mensaje : ")
    client_socket.send((mensaje.encode()))

    if mensaje == "exit":
        flag = False
    else :
        data = client_socket.recv(1024)
        print(f"Mensaje recibido : {data.decode()}")

client_socket.close()
print("Finalizando Client....")

