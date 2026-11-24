import socket

ip = "localhost"
port = 1234

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((ip,port))
server_socket.listen(2)
print(  f"Escuchando... {ip},{port}")

banderia = True
while banderia:
    conn,client_address  = server_socket.accept()
    print(f"Connecting..... {client_address}")
    
    flag =True
    while flag:
        
        data = conn.recv(1024)

        if not data:
            flag = False
        else:
                mensaje = data.decode()
                print(f"Mensaje recibido : {data.decode()}")       
                if mensaje == "exit":
                    flag = False
                else:
                    conn.send(data) 


    conn.close()

