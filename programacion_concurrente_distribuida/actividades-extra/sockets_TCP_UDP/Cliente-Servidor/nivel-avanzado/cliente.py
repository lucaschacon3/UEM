import socket

ip ="127.0.0.1"
port = 1234

c_s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
c_s.connect((ip,port))


flag = True

while flag:

    msg = input("admin : ")
    c_s.send(msg.encode())

    contraseña = input("contraseña : ")
    c_s.send(contraseña.encode())


    data = c_s.recv(1024)
    print(f"Respuesta => {data.decode()}")

    if msg == "exit":
        flag = False