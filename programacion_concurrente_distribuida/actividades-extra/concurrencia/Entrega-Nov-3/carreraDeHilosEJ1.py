import threading
import random
import time

def iniciar(numCorredores):
    corredores = []
    for i in range(numCorredores):
        corredores.append(threading.Thread(target = mover_Corredor, name = "Hilo " + str(i+1)))

    for x in corredores:
        x.start()

    for x in corredores:
        x.join()
    

def mover_Corredor():
    global ganador
    banderaInicial = bandera.wait()

    if banderaInicial == 0:
        mutex.acquire()
        print("La carrera ha comenzado!")
        mutex.release()
    
    time.sleep(1)

    distanciaRecorrida = 0
    while distanciaRecorrida < 100:
        distanciaRecorrida += random.randint(0,10)
        if mutex.acquire():
            print(threading.current_thread().name + " lleva " + str(distanciaRecorrida) + " metros")
            mutex.release()
        time.sleep(1)

    print(threading.current_thread().name + " ha terminado")

    if not ganador:
        ganador = True
        bandera.wait()
        print(threading.current_thread().name + " ha ganado!")

    else:
        bandera.wait()

numero = int(input("Introduce el numero de corredores: "))
bandera = threading.Barrier(numero)
ganador = False
mutex = threading.Lock()

iniciar(numero)
print("La carrera ha terminado")

