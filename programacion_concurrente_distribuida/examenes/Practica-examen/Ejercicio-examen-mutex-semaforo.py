import threading 
import time 
import random

mutex =threading.Lock()
s = threading.Semaphore(1)

def hola():
    for i in range(4):
        s.acquire(timeout=2)
        mutex.acquire(timeout=2)
        print (f"{i+1}Gino")
        mutex.release()
        s.release()
        time.sleep(1)


lista= []

for i in range(1):
    h1 = threading.Thread(target=hola)
    lista.append(h1)
    h1.start()

for i in lista:
    i.join()


    

