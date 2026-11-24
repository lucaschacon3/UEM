import socket

server_ip = "127.0.0.1"
server_port = 12345

servidor_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

servidor_socket.bind((server_ip,server_port))
servidor_socket.listen(1)
print(f"Escuchando Client {server_ip},{server_port}")

conn,client_address = servidor_socket.accept()
print(f"Conexion  de {client_address}")

flag = True

while flag:

    data = conn.recv(1024)
    print(f"Mensaje recibido : {data.decode()}")

    if data.decode() == "exit" :
        flag = False
    else:
        mensaje = input("Escribe mensaje : ")
        conn.send(mensaje.encode())

conn.close()
servidor_socket.close()
print("Finalizando Servidor....")