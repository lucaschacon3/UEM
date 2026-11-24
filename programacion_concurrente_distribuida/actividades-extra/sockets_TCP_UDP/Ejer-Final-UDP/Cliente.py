import socket

ip = "127.0.01"
port = 1234

c_s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

flag = True

while flag :

    mensaje = input("Enviar mensaje a Servidor : ")
    c_s.sendto(mensaje.encode(),(ip,port))

    if mensaje == "salir":
        flag = False
    else:
        dato,address = c_s.recvfrom(1024)
        print(f"Mensaje recibido  de servidor: {dato.decode()}")



c_s.close()