# 5.2 — 2 productores con parámetros
#Crea un programa con:
#Una lista compartida llamada tareas (vacía).
#Un Lock para proteger la lista.
#2 hilos PRODUCTORES (P1 y P2):

#Cada productor añade 5 tareas a la lista.
#Espera 1 segundo entre cada tarea.
#El productor recibe su nombre por parámetro ("P1" o "P2").
#Las tareas se llaman: "P1_Tarea_1", "P1_Tarea_2"... y "P2_Tarea_1", "P2_Tarea_2"...
#Imprime cuando añade cada tarea.

#1 hilo CONSUMIDOR:
#Revisa la lista cada 0.5 segundos.
#Si hay tareas → saca la primera con pop(0) y la imprime.
#Si NO hay tareas → simplemente espera y vuelve a revisar.
#Termina cuando ha procesado 10 tareas en total (5+5).

#El programa principal:

#Crea los 3 hilos (2 productores + 1 consumidor).
#Los arranca con start() y espera con join().
#Imprime "TERMINANDO TAREAS..." al final.


import threading 
import time

tareas = []
mutex = threading.Lock()

def productor(nombre):

    for i in range(5):
        time.sleep(1)
        mutex.acquire()
        tareas.append(f"{nombre}_Tareas_" + str(i+1))
        print(f"PRODUCTOR {nombre}")
        mutex.release()

def consumidor():
    procesando = 0

    while procesando < 10:
        time.sleep(.5)
        mutex.acquire()
        if len(tareas) > 0:
            t = tareas.pop(0)
            procesando +=1
            print(f"CONSUMIDOR => {t} : {procesando} ")
        mutex.release()



h1 = threading.Thread(target=productor,args=("P1",))
h2 = threading.Thread(target= productor,args =("P2",))
h3 = threading.Thread(target=consumidor)

h1.start()
h2.start()
h3.start()

h1.join()
h2.join()
h3.join()

print("FINALIZANDO TAREAS...")

