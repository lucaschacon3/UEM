"""Simula una carrera de hilos en Python. 
Crea varios hilos que representan corredores en una pista y haz que
compitan para llegar a la línea de meta. Utiliza mecanismos de
sincronización para asegurarte de que los hilos compitan de manera 
justa y que solo uno pueda ganar la carrera
"""
import threading
import time
import random

NUM_TORTUGAS = 7

#Bloque para sincronizacion y variables compartidas
lock = threading.Lock()
carrera_terminada = False
resultados = []  #lista para registrar el orden de llegada

#Función que simula la carrera de cada tortuga
def tortugas(nombre):
    global carrera_terminada
    print(nombre, " ha salido a correr...")
    ha_llegado = False  #variable booleana para indicar si la tortuga llegó a la meta
    while not carrera_terminada and not ha_llegado:
        #Tiempo que la tortuga tarda en avanzar un poco
        tiempo_corrida = random.uniform(0.5, 1.5)
        time.sleep(tiempo_corrida)

        #La tortuga avanza
        print(nombre," está corriendo...")

        #Verificacion si llega a la meta
        if random.random() < 0.3:  #30% de probabilidad de llegar a la meta en cada ciclo
            with lock:
                if nombre not in resultados:  #solo agregamos si la tortuga no ha llegado antes
                    resultados.append(nombre)
                    ha_llegado = True  #la tortuga ha llegado a la meta
                    if len(resultados) == NUM_TORTUGAS:
                        carrera_terminada = True  #finaliza la carrera cuando todos llegan

#Se crea y lanza los hilos para cada corredor
hilos = []

for i in range(NUM_TORTUGAS):
    nombre_corredor = f"Tortuga {i+1}"
    hilo = threading.Thread(target=tortugas, args=(nombre_corredor,))
    hilos.append(hilo)
    hilo.start()

#Se espere a que todos los hilos terminen la carrera
for hilo in hilos:
    hilo.join()

#Imprime los resultados finales
print("\nResultados de la carrera:")
for i, tortuga in enumerate(resultados):
    posicion = i + 1
    if posicion == 1:
        print("La ", tortuga, " llegó en primer lugar y ganó la carrera")
    elif posicion == 2:
        print("La ", tortuga, " llegó en segundo lugar")
    elif posicion == 3:
        print("La ", tortuga, " llegó en tercer lugar")
    else:
        print("La ", tortuga," llegó en la posición ", posicion)
