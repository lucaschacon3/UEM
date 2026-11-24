import socket

ip = "127.0.01"
port = 1234

s_s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s_s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s_s.bind((ip,port))

print(f"Escuchando....(){ip},{port}")

flag = True

while flag:

    dato,address = s_s.recvfrom(1024)
    mensaje = dato.decode()
    print(f"Mensaje recibido  de Cliente => {mensaje}")

    if mensaje == "salir":
        flag = False
    else:
        resp = input("Enviar mensaje Cliente : ")
        s_s.sendto(resp.encode(),(address))
        

s_s.close()

