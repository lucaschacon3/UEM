"""
Escribir el código de un programa "Carreras de las tortugas", el cual es un simulador de una carrera de tortugas 
en el que varias "tortugas" se mueven de manera aleatoria hasta que una de ellas alcanza la meta. 
Aquí hay un resumen de lo que ocurriría:

1. Al ejecutar el programa, se crearán múltiples hilos asociados a las tortugas en la forma que se desee.
2. En cada iteración de mover_tortuga(), cada tortuga generará una velocidad aleatoria y avanzará una distancia aleatoria. 
Esto simula el progreso de cada tortuga en la carrera.
3. El programa mostrará el progreso de cada tortuga en la consola, indicando cuántos metros ha recorrido cada una.
4. Las tortugas continuarán moviéndose de manera aleatoria hasta que una de ellas alcance o supere los 100 metros, 
que es la distancia de la meta.
5. Una vez que una tortuga haya cruzado la meta, el programa mostrará un mensaje indicando que esa tortuga ha ganado la carrera.
6. Finalmente, el programa esperará a que todos los hilos hayan terminado de ejecutarse antes de finalizar.

El resultado específico puede variar en cada ejecución debido a la aleatoriedad en la velocidad y el progreso de las tortugas. 
Puede que una tortuga gane en una ejecución y otra en la siguiente.


"""

import threading
import time
import random

DISTANCIA_META = 100

clasificion = []

def mover_tortuga(nombre, progreso):
    inicio = time.time()
    terminar_carrera = False
    while terminar_carrera == False:
        distancia_aleatoria = random.randint(1, 20)  # Velocidad aleatoria entre 1 y 20 metros
        progreso += distancia_aleatoria
        print(f"{nombre} ha avanzado {distancia_aleatoria} metros. Progreso total: {progreso} metros.")
        time.sleep(random.randint(1, 2))  # Pausa aleatoria entre movimientos
        if progreso >= DISTANCIA_META:
            terminar_carrera = True

    tiempo_total = time.time() - inicio
    clasificion.append((nombre, tiempo_total))

hilos = []

for i in range(3):
    hilo = threading.Thread(
        target=mover_tortuga,
        args=(f"Tortuga-{i}", 0),
        name=f"Worker-{i}"
    )
    hilos.append(hilo)  
    hilo.start()       


for hilo in hilos:
    hilo.join()

print("--------------------------------")
clasificacion_ordenada = sorted(clasificion)
print("Ha ganado la carrera la tortuga: ", clasificacion_ordenada[0][0], " con un tiempo de: ", clasificacion_ordenada[0][1], " segundos.")
