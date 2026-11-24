"""Imagina un restaurante con un número limitado de mesas disponibles. 
Los clientes (hilos) llegan al restaurante y desean sentarse en una mesa. 
Crea un programa que utilice semáforos para coordinar el acceso de los 
clientes alas mesas y asegurarte de que el restaurante no exceda su capacidad
"""

import threading
import time
import random

# Parámetros
NUM_DE_MESAS = 5
mesas = ["libre" for _ in range(NUM_DE_MESAS)]  #sstado de las mesas
CLIENTES = 10  # Número de clientes (hilos)
camarero = threading.Semaphore(NUM_DE_MESAS)  #semáforo para las mesas disponibles

def EntrarAComer(nombre):
    global camarero
    global mesas

    terminado = False
    while not terminado:
        if camarero.acquire(timeout=2):  #se trata de adquirir una mesa
            mesa_asignada = False  #control de si el cliente ha encontrado mesa

            #Busca una mesa libre
            for k in range(NUM_DE_MESAS):
                if mesas[k] == "libre" and not mesa_asignada:
                    mesas[k] = nombre  #ocupa la mesa
                    mesa_asignada = True
                    print(nombre + " ha tomado la mesa " + str(k + 1) + " para comer.")

                    #Simulacion de tiempo comiendo
                    time.sleep(random.randint(1, 3))

                    print(nombre + ": Hemos terminado de comer en la mesa " + str(k + 1))
                    mesas[k] = "libre"  #se libera la mesa
                    terminado = True  #se indica que el cliente ha terminado
                    camarero.release()  #se libera el semáforo para que otro cliente pueda usar la mesa
                    mesa_asignada = False  #s resetea para futuras iteraciones

            #Si no se asignó mesa, liberar el semáforo
            if not mesa_asignada:
                camarero.release()  #se libera si no se asignó ninguna mesa
        else:
            print(nombre + ": No hay mesas disponibles, esperando...")
            time.sleep(1)

#Funcion para revisar el estado del restaurante
def revisarRestaurante():
    while True:
        print("Estado de mesas: " + str(mesas))
        time.sleep(2)

#Se crea y lanza los hilos de clientes
hilos_clientes = []
for c in range(1, CLIENTES + 1):
    hilo = threading.Thread(target=EntrarAComer, args=("Cliente_" + str(c),))
    hilos_clientes.append(hilo)

#Hilos de revisión y clientes
revisor = threading.Thread(target=revisarRestaurante, daemon=True) #hilo para mostrar el estado del restaurante
revisor.start()

for hilo in hilos_clientes:
    hilo.start()

for hilo in hilos_clientes:
    hilo.join()  # Espera a que todos los hilos de clientes terminen
