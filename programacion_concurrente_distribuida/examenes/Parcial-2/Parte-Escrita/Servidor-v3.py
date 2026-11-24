import socket

ip = "127.0.0.1"
port = 1234

s_s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s_s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s_s.bind((ip,port))
s_s.listen()
print(f"Escuchando.... {ip}{port}")

conn ,  address = s_s.accept()
print(f"Connecting with.... {address}")

archivo = conn.makefile("r")

flag = True

suma = 0

while flag:

    linea = archivo.readline()

    if not linea:
        flag = False

    else:
        msg = linea.strip()

        if msg == "FIN":
            conn.send((str(suma) + "\n").encode())
            flag =False

        else:
            n = int(msg)
            suma += n
            conn.send(b"OK\n")

conn.close()
s_s.close()

