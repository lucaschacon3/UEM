import socket   
import random
import threading 

ip = "127.0.0.1"
port = 1234

c_s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
c_s.connect((ip,port))

def client():

    for _ in range(5):

        n = random.randint(1,9)
        print(f"Numeros =>{n}")
        c_s.send((str(n) + "\n").encode())

        ok = c_s.recv(1024).decode()
        print(f"Recibimos OK : {ok}")



    c_s.send(b"FIN\n")
    suma = c_s.recv(1024).decode()
    print(f"Finalizando ..... SUMA => {suma} ")

h1 = threading.Thread(target=client)
h1.start()
h1.join()