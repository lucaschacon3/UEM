import socket
import random
import time

ip = "localhost"
port = 1234

cliente_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

flag = True
while flag:


    temperatura = random.randint(20,35)

    estado = "OK"

    if temperatura >= 35:
        estado = "ALERTA"

    mensaje = f"temperatura={temperatura} , estado ={estado}"
    cliente_socket.sendto(mensaje.encode(),(ip,port))

    time.sleep(1)


