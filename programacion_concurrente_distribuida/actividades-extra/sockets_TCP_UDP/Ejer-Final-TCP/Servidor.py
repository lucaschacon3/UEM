import socket


ip = "localhost"
port = 1234

server_s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server_s.bind((ip,port))
server_s.listen(2)
print(f"Escuchando.... {ip},{port}")

conn,address = server_s.accept()
print(f"Connecting... {address}")

flag = True

while flag :

    dato = conn.recv(1024)
    print(f"Mensaje recibido : {dato.decode()}")
    if dato.decode() == "salir":
        flag = False
    else:
        r = input("Enviar mensaje : ")
        conn.send(r.encode())

server_s.close()



    




