import threading
import random
import time

META = 100
ganador = None
carrera_en_curso = True  
lock = threading.Lock()

def mover_tortuga(nombre):
    global ganador, carrera_en_curso
    distancia = 0
    
    while carrera_en_curso:
        time.sleep(0.2)
        avance = random.randint(1, 10)
        distancia += avance
        
        lock.acquire()
        try:
            print(nombre + " lleva " + str(distancia) + " metros")
            
            if ganador is None and distancia >= META:
                ganador = nombre
                carrera_en_curso = False
                print("\n " + ganador + " ha ganado la carrera\n")
        finally:
            lock.release()

nombres_tortugas = ["tortuga_1", "tortuga_2", "tortuga_3", "tortuga_4"]
hilos = []

for nombre in nombres_tortugas:
    hilo = threading.Thread(target=mover_tortuga, args=(nombre,))
    hilos.append(hilo)
    hilo.start()


for hilo in hilos:
    hilo.join()

print("La carrera ha terminado")
