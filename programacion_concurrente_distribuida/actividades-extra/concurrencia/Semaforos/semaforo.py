import time 
import random
import threading

semaphore = threading.Semaphore()
mensaje = ""

def cantar():
    global mensaje
    hecho = False
    while not hecho:
        if semaphore.acquire(timeout=2):
            mensaje = mensaje + " DoReMiFaSol"
            print(f"{mensaje} ")
            semaphore.release()
            hecho = True
        else:
            print("shhhh")
            time.sleep(random.randint(3,5)/10)

listaH = []

for i in range(6):
    t = threading.Thread(target=cantar)
    listaH.append(t)

for s in listaH:
    s.start()

for j in listaH:
    j.join()

print("terminao")