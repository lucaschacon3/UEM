import threading
import time
import random
import math

# variables globales
listNums = []
maxVal = 100
numHilos = 3
hilos = []
semaforo = threading.Semaphore()  
mutex = threading.Lock()    

# Funcion para contar
def contar(yo):
    global maxVal
    global listNums
    n = 0
    while n <= maxVal:
        if semaforo.acquire(timeout=2):  
            n += 1
            listNums[yo] = n 
            semaforo.release()  
        time.sleep(random.randint(2, 5))  

# Funcion para pintar el progreso
def pintar(maxVal, numH):
    global listNums
    while True:
        x = 0
        if semaforo.acquire(timeout=2):  
            mutex.acquire()  
            for i in listNums:
                x += i  
            porcentaje = x * 100 / (maxVal * numH)
            porcentaje = math.ceil(porcentaje)
            print(listNums, f"{porcentaje}%")
            mutex.release()  
            semaforo.release()  
        time.sleep(2)  


for i in range(numHilos):
    hilo = threading.Thread(target=contar, args=[i,])
    hilos.append(hilo)
    listNums.append(0)

# hilo para pintar el progreso
hilo = threading.Thread(target=pintar, args=[maxVal, numHilos])
hilos.append(hilo)


for s in hilos:
    s.start()


for l in hilos:
    l.join()














