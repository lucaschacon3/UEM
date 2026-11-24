# Mini-ejercicio 5 — Una práctica más
# Lista compartida tareas = []
# Lock para protegerla
# 1 productor: añade 10 tareas (1 cada segundo) tipo "Tarea 1", "Tarea 2"...
# 1 consumidor: revisa cada 0.5s, saca con pop(0), termina al procesar 10
# 2 hilos en total: start() y join()
# Print final "FINALIZANDO TAREAS..."
#Sin with, break, continue, pass

import threading
import time

tareas= []
mutex = threading.Lock()

def productor():
    for i in range(10):
        time.sleep(1)
        mutex.acquire()
        tareas.append("TAREA : " + str(i+1))
        print(f"PRODUCTOR : {tareas}")
        mutex.release()

def consumidor():
    procesando = 0
    while procesando < 10:
        time.sleep(.5)
        mutex.acquire()
        if len(tareas) > 0:
            t = tareas.pop(0)
            procesando += 1
            print(f"CONSUMIDOR : {t} / {procesando}")
        mutex.release()


h1=threading.Thread(target=productor)
h2 = threading.Thread(target=consumidor)

h1.start()
h2.start()

h1.join()
h2.join()

print("TERMINANDO TAREAS....")


