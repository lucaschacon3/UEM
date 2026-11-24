import socket

ip = "localhost"
port = 1234

cliente_s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
cliente_s.connect((ip,port))

flag = True
while flag :

    mensaje = input("Escribir mensaje a server : ")
    cliente_s.send(mensaje.encode())
    
    if mensaje == "salir":
        flag = False
    else:
        dato = cliente_s.recv(1024)
        print(f"Mensaje recibido : {dato.decode()}")


cliente_s.close()



