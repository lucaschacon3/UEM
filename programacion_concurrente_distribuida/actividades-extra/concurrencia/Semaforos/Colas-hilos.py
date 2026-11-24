import threading
from time import sleep
import random
import queue

cola = queue.Queue()
mutex = threading.Lock()
contador = 0
def escribir():
    for i in range(20):
        if mutex.acquire(blocking = True, timeout = 0.1):
            cola.put(str(i) + " " + threading.current_thread().name)
            sleep(random.randint(1,500)/10000)
            mutex.release()
        else:
            print(threading.current_thread().name + " no ha escrito " + str(i))
        

def leer():
    global contador
    while not cola.empty():
        print(cola.get())
        sleep(random.randint(1,500)/10000)
        contador += 1
        
        
      


hilos = []
print("Cuantos hilos escritores quieres?")
nHilos = input()
nHilos = int(nHilos)

for i in range (nHilos):
    hilos.append(threading.Thread(target = escribir, name = "escritor " + str(i+1)))

hilos.append(threading.Thread(target = leer, name = "lector"))

for x in hilos:
    x.start()

for x in hilos:
    x.join()

print("Terminado, se lograron leer " + str(contador) + " valores")
print(contador == 20*nHilos)