"""Implementa un problema de productor-consumidor donde los productores 
generan elementos con características específicas y los consumidores 
solo pueden tomar elementos que cumplan con ciertos criterios. 
Utiliza una cola bloqueante para gestionar la comunicación entre productores y consumidores
"""
import threading
import queue
import random
import time

CANT_PRODUCTORES = 3
CANT_CONSUMIDORES = 2
cola = queue.Queue(maxsize=7)  #tamaño máximo de la cola
TIEMPOR_EJECUCION = 5  #tiempo total de ejecución en segundos

#Criterio de consumo como una función
def criterio_consumo(elemento):
    return elemento % 2 == 0  #solo consumir si es par

#Función del productor
def productor(id_producto):
    while time.time() < end_time:  #continuar hasta que termine el tiempo
        elemento = random.randint(1, 100)
        print("Productor ", id_producto , " ha producido: ", elemento)
        cola.put(elemento)
        time.sleep(random.uniform(0.1, 1))

#Función del consumidor
def consumidor(id_consumidor):
    while time.time() < end_time or not cola.empty():  #continuar hasta que termine el tiempo o la cola esté vacía
        if not cola.empty():
            elemento = cola.get()
            if criterio_consumo(elemento):
                print("Consumidor ", id_consumidor ," ha consumido: ", elemento)
            else:
                print("Consumidor ", id_consumidor ," ha rechazado: ", elemento)
            cola.task_done()
        time.sleep(random.uniform(0.1, 1.5))

#Tiempo de finalización
end_time = time.time() + TIEMPOR_EJECUCION

#Se crea y lanza los hilos de los productores
for i in range(CANT_PRODUCTORES):
    hilo_productor = threading.Thread(target=productor, args=(i + 1,))
    hilo_productor.daemon = True
    hilo_productor.start()

#Se crea y lanza los hilos de los consumidores
for i in range(CANT_CONSUMIDORES):
    hilo_consumidor = threading.Thread(target=consumidor, args=(i + 1,))
    hilo_consumidor.daemon = True
    hilo_consumidor.start()

#Esperar hasta que todos los elementos hayan sido consumidos o se acabe el tiempo
cola.join()

print("El tiempo de ejecución ha terminado.")
