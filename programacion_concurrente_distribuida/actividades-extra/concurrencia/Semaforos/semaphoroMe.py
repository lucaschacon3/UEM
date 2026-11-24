import threading 
import time
import random

s = threading.Semaphore()
mensaje =""

def cantar():
    global mensaje
    hecho = False
    while not hecho:
        if s.acquire(timeout=2):
            mensaje = mensaje + "DoReMiFaSol"
            print(f"{mensaje}")
            s.release()
            hecho = True
        else:
            print("shhh")
            time.sleep(random.randint(3,5)/10)

listaH = []

for i in range(5):
    h1 = threading.Thread(target=cantar)
    listaH.append(h1)

for k in listaH:
    k.start()

for j in listaH:
    j.join()

