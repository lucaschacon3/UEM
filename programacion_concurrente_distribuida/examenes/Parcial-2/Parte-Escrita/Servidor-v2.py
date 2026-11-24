import socket

ip = "127.0.0.1"
port = 1234

servidor_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

servidor_socket.bind((ip,port))
servidor_socket.listen(1)

print(f"Escuchando : {ip},{port}")

conn,client_address = servidor_socket.accept()

print(f"Conectado : {client_address}")

archivo =  conn.makefile("r")

flag = True
suma = 0

while flag:

    line = archivo.readline()

    if not line:
        flag = False

    else:
        mensaje = line.strip()

        if mensaje == "FIN":
            flag = False
        else:
            suma += int(mensaje)
            conn.sendall(b"OK\n")

print(f"SUMA => {suma}")
conn.close()
servidor_socket.close()


