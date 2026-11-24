import socket


server_ip = "127.0.0.1"
server_port = 1234

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((server_ip,server_port))
server_socket.listen(1)

print(f"Escuchando => {server_ip},{server_port}")

conn,client_address = server_socket.accept()
print(f"Conectado => {client_address}")
suma = 0
archivo = conn.makefile("r")
flag = True

while flag :

    line = archivo.readline()

    if not line:
        flag =False
    else:
        mensaje = line.strip()

        if mensaje == "FIN":
            flag = False
        else:
            if mensaje.isdigit():
                suma += int(mensaje)
                conn.send(b"OK\n")

conn.close()
server_socket.close()




