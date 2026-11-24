#1.3 - 10 hilos incrementando un contador global SIN sincronización (observar el caos)
#Mismo que 1.3 pero CON threading. Lock() usando acquire() y release ()
import threading
import time
import random

contador = 0
mutex = threading.Lock()

def contamos(nombre):
    global contador

    for i in range(5):
        mutex.acquire()
        valor = contador
        time.sleep(random.uniform(1,.3))
        print(f"{nombre} CONTAMOS {contador}")
        contador = valor + 1
        mutex.release()

hilos = []

for i in range(10):

    hilo = threading.Thread(target=contamos, args=("HILO_" + str(i+1),))
    hilos.append(hilo)
    hilo.start()

for i in hilos:
    i.join()

print("TERMINANDO CONTADOR ")
