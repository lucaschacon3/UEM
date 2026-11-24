import socket
import threading

ip ="127.0.0.1"
port = 1234

id = "admin"
pas = "1234"

def atender_cliente(conn):
    intento = 0

    while intento < 3 :
        flag =False

        user = conn.recv(1024).decode()
        contrasena = conn.recv(1024).decode()

        if user == id and contrasena == pas:
            conn.send("BIENVENIDO.... ".encode())
            flag = True
        else:
            intento += 1
            conn.send(f"Error".encode())

    if intento == 3:
        conn.send("Demasiado intentos".encode())
        
    conn.close()

s_s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s_s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s_s.bind((ip,port))
s_s.listen(2)
print(f"Escuchando... {ip},{port}")

while True:

    conn,address = s_s.accept()
    print(f"Connecting...{address}")

    h1 = threading.Thread(target = atender_cliente , args = (conn,))
    h1.start()










