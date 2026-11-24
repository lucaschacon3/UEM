import threading
from time import sleep
from random import randint

def iniciar(nClientes):
    hilos = []
    for i in range (nClientes):
        hilos.append(threading.Thread(target = restaurante, name = "cliente " + str(i+1)))
    hilos.append(threading.Thread(target = estado))

    for x in hilos:
        x.start()

    for x in hilos:
        x.join()

def restaurante():
    global mesas, maxCapacidad, mecero, mutex, clientesAtendidos
    comer = False
    
    print(threading.current_thread().name + " ha llegado al restaurante")
    
    while not comer:
        sleep(randint(3,5))

        if mecero.acquire(timeout=2):

            for i in range(maxCapacidad):

                if mesas[i] and not comer:
                    mesas[i] = False

                    if mutex.acquire():
                        print(threading.current_thread().name + " esta en la mesa " + str(i+1))
                        mutex.release()
                    
                    sleep(randint(5,8))
                    mesas[i] = True
                    comer = True
                    clientesAtendidos += 1

                    if mutex.acquire():
                        print(threading.current_thread().name + " se ha ido")
                        mutex.release()
                    
                    mecero.release()
        
        elif mutex.acquire():
            print(threading.current_thread().name + ", no he podido conseguir mesa, voy a preguntar otra vez.")
            mutex.release()

def estado():
    global mutex, mesas, numClientes, clientesAtendidos

    while clientesAtendidos != numClientes:
        sleep(5)

        if mutex.acquire(timeout=1):
            print("Mesas en el restaurante:")
            print(mesas)
            mutex.release()


numClientes = int(input("Introduce el numero de clientes: "))
maxCapacidad = int(input("Introduce la maxima capacidad del restaurante: "))
mecero = threading.Semaphore(maxCapacidad)
mutex = threading.Lock()
clientesAtendidos = 0

mesas = []
for i in range(maxCapacidad):
    mesas.append(True)

iniciar(numClientes)
print("Terminamos la simulacion del restaurante")