# 1.2 — 3 hilos imprimiendo su nombre y números del 1 al 5 con retardo aleatorio

import threading
import time 
import random

Mutex = threading.Lock()

def imprimiendo(nombre):
    i = 1
    while i <= 5:
        Mutex.acquire()
        print(f"[{nombre}] => NUMEROS {i}")
        time.sleep(random.uniform(0,0.3))
        print(f"{nombre} Terminado")
        i+= 1
        Mutex.release()

h1 = threading.Thread(target=imprimiendo,args=("HILO_1",))
h2 = threading.Thread(target=imprimiendo,args=("HILO_2",))
h3 = threading.Thread(target=imprimiendo,args=("HILO_3",))

h1.start()
h2.start()
h3.start()
h1.join()
h2.join()
h3.join()


print("TERMINANDO EJECUCION")







