"""EJEMPLO - BARRERA"""

import threading
import time
import random

#Creacion de barrera simple para 3 hilos
barrera = threading.Barrier(3)

#Funcion q ejecutara cada hilo
def tarea(id_hilo):
    """Función que simula una tarea y sincroniza los hilos en una barrera"""

    print("Hilo" , id_hilo, " esta realizando una tarea")
    time.sleep(random.uniform(1,3)) #para simular el trabajo con una espera aleatoria(decimales)

    print("Hilo", id_hilo, " ha llegado a la barrera")
    barrera.wait() #cada hilo espera o detiene en la barrera hasta que los 3 lleguen

    print("Hilo", id_hilo, " pasa la barrera y continua con la ejecución") #cada hilo cntinua una vez q todos han llegado

#Lista de hilos (sin ejecutarlos todavía)
hilos = [] #lista vacia

for i in range(3):
    hilo = threading.Thread(target=tarea, args=(i,)) #creacion de hilo
    hilos.append(hilo) #para agregar los hilos a la lista

#Inicializar y ejecutar los hilos
for hilo in hilos:
    hilo.start() #ejecuta la funcion "tarea" en cada hilo

#Esperar q todos lo hilos terminen su ejecucion
for hilo in hilos:
    hilo.join() #el programa principal espera hasta que cada hilo termine antes de continuar


# OJO:
# La barrera hace que todos los hilos esperen en el mismo punto (sincronización)
# una vez q todos los hilos han llegado a la barrera, esta se "rompe" y permite que todos continúen.
# El orden de salida de los hilos NO está controlado por la barrera ni por el código,
# sino por el sistema operativo, que decide cuál hilo ejecutarse primero después de la barrera.
