import threading
from time import sleep
import random
s = threading.Semaphore()
mutex = threading.Lock()
sumaGlobal = 0
def modRecurso():
    global sumaGlobal
    global s
    i = 0
    while i < 20:
        if s.acquire(timeout=2/100):
            sumaGlobal += 1
            sleep(random.randint(1,500)/10000)
            print("Soy " + threading.current_thread().name + ", la suma es de " + str(sumaGlobal))
            s.release()
        else:
            print("Soy " + threading.current_thread().name + ", no logre acceder en mi intento " + str(i+1))
        i += 1

hilos = []
nHilos = 4
for i in range (nHilos):
    hilos.append(threading.Thread(target = modRecurso, name = "hilo " + str(i+1)))

for x in hilos:
    x.start()

for x in hilos:
    x.join()
