import queue
import threading
import time
import random


cant_gallinas_inicial = 5
gallinas = []
huevos = []
sinHuevo = []
criadero = queue.Queue()
lock1 = threading.Lock()
barrera = threading.Barrier(1)
contador = 0


semaforo = threading.Semaphore(cant_gallinas_inicial)

for l in range(cant_gallinas_inicial):
    gallinas.append(cant_gallinas_inicial)

#Funcion Ejer1
def gallina():
    global contador
    print("Descansando..")
    for i in range(5):
        if random.randint(0,1) >= 0.82:
            print("Dia " ,i+1 ," Hay huevo")
            semaforo.acquire()
            lock1.acquire()
            huevos.append(1)
            # if (random.randint(1,300)) / 365 < 0.02:
            #     print("Dia " , i+1, " Al criadero")
            #     criadero.put(1)
            lock1.release()
            semaforo.release()
        elif (random.randint(1,300)) / 365 >= 0.18:
            print("Dia " ,i+1 ," No hay huevo")
            semaforo.acquire()
            lock1.acquire()
            sinHuevo.append(1)
            lock1.release()
            semaforo.release()

    time.sleep(random.randint(1,3))

#Funcin Ejer3
def imprimir():
    print("Gallinas Total: ", len(gallinas))
    print("Huevos Total: ", len(huevos))
    print("Sin Huevos Total: ", len(sinHuevo))
    # print("Criadero Total: " + criadero.get())
    # barrera.wait()
    # print("Super Total: ", contador = contador + len(huevos))




hilo1 = threading.Thread(target=gallina, args=())

hilo1.start()


hilo1.join()


imprimir()

for j in range(cant_gallinas_inicial-1):
    print("\n")
    gallina()
    imprimir()
    print("\n")
