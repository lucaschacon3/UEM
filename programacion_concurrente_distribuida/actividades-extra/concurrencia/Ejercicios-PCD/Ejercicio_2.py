#1.3 - 10 hilos incrementando un contador global SIN sincronización (observar el caos)

import threading 
import time
import random

contador = 0
mutex = threading.Lock()

def contamos(nombre):
    global contador

    for i in range(5):

        valor = contador
        time.sleep(random.uniform(0,.3))
        print(f"{nombre} contador {contador}")
        contador = valor + 1

hilos = []


for i in range(10):
    hilo = threading.Thread(target = contamos,args=("HILO" + str(i+1),))
    hilos.append(hilo)
    hilo.start()

for i in hilos:
    i.join()

print(f"terminando contador {contador}... ")



