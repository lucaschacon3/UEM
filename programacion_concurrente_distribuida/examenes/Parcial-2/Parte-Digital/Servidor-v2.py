#EXAMEN DIGITAL PCD

import socket
import threading
import random
import time

ip = "localhost"
port = 1234

maximo = 9
mutex = threading.Lock()
lista = []

def manejar_cliente(conn,indice):
    totalsuma = 0
    archivo = conn.makefile("r")

    flag =True

    while flag:

        linea =archivo.readline()

        if not linea:
            flag = False
        else:
            msg = linea.strip()

            if msg == "FIN":
                conn.send((str(totalsuma) + "\n").encode())
                flag = False
            else:
                numero = int(msg)
                totalsuma += numero
                lista[indice] = totalsuma

                if numero >= maximo:
                    conn.send(b"MAX\n")
                else:
                    time.sleep(random.randint(2,5))
                    conn.send(b"OK\n")

    conn.close()


def main():

    s_s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s_s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s_s.bind((ip,port))
    s_s.listen()
    
    print(f"Escuchando.....{ip}{port}")

    while True:

        conn,address= s_s.accept()
        print(f"Connecting.......{address}")

        mutex.acquire()
        indice = len(lista)
        lista.append(0)
        mutex.release()

        h1 = threading.Thread(target=manejar_cliente,args=(conn,indice))
        h1.start()


main()











