import socket

ip = "localhost"
port = 1234

server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

server_socket.bind((ip,port))
print(f"Escuchando....  {ip},{port}")

while True:

    conn,address = server_socket.recvfrom(1024)

    data = conn.decode()
    print(f"Mensaje recibido : {data}")

    f = open("file.txt" , "a" , encoding="utf-8")
    f.write(f"{address[0]},{address[1]} : {data} \n")
    f.close()

