import queue
import threading
from time import sleep
from random import randint

coches = 5
carriles = 1
tramoA = queue.Queue(5)
cruce = queue.Queue(3)
mundo = queue.Queue(10)
desguace = queue.Queue()
sCruce = threading.Semaphore(carriles)
sMundo = threading.Semaphore(carriles)
sRegreso = threading.Semaphore(carriles)
sDesguace = threading.Semaphore(carriles)
mutex = threading.Lock()

class coche:
    def __init__(self, nombre, velocidad, vueltas):
        self.nombre = nombre
        self.velocidad = velocidad
        self.vueltas = vueltas
    
def generador():
    global coches, lista
    for i in range(coches):
        tramoA.put(["coche_" + str(i+1), 0.0, 0])

def cruzar():
    global tramoA, cruce, sCruce
    i = 0
    while not tramoA.empty():
        if sCruce.acquire(timeout=1) and not cruce.full():
            cruce.put(tramoA.get())
            print("Soy " + threading.current_thread().name + ", he cruzado un coche")
            sCruce.release()
            sleep(randint(1,50)/100)
        elif cruce.full():
            print("Soy " + threading.current_thread().name + ", el cruce esta lleno")
        else:
            print("Soy " + threading.current_thread().name + ", mi coche no pudo cruzar")
        i += 1

def estado():
    global cruce
    i = 0
    while not tramoA.empty():
        sleep(2)
        if mutex.acquire():
            print(cruce.queue)
            print(tramoA.queue)
            mutex.release()
        else:
            print("No he podido acceder a la pantalla")

def generar():
    i = 0
    while i < 100:
        sleep(randint(20,50))
        if not tramoA.full():
            tramoA.put(["coche_" + str(i+6), 0.0, 0])
            i += 1
        else:
            print("TramoA lleno")


generador()
hilos = []
nHilos = 3
for i in range (nHilos):
    hilos.append(threading.Thread(target = cruzar, name = "hilo " + str(i+1)))
hilos.append(threading.Thread(target = estado, name = "hiloCruce"))
hilos.append(threading.Thread(target = generar, name = "hiloGenerar"))

for x in hilos:
    x.start()

for x in hilos:
    x.join()

