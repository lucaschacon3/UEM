import threading
import time 
import random

parking  = threading.Semaphore(3)

def semaforos(nombre):
    print(f"{nombre} llega")
    time.sleep(1)
    parking.acquire()
    print(f"{nombre} aparcado")
    time.sleep(3)
    print(f"{nombre} se va...")
    parking.release()


hilos = []

for i in range(8):
    hilo = threading.Thread(target=semaforos,args=("COCHE_" + str(i+1),))
    hilos.append(hilo)
    hilo.start()

for i in hilos:
    i.join()

print(f"TERMINANDO CARRERA...")
