"""
Simulador de una carrera de tortugas con hilos.

Cada tortuga corre en su propio hilo y avanza distancias aleatorias hasta
cruzar la meta (100 m). El primer hilo que llega declara el ganador con un
Lock/Event, detiene la carrera al momento y el resto de hilos finaliza.
"""

import threading
import time
import random

DISTANCIA_META = 100

clasificacion = []
lock = threading.Lock()
evento_fin = threading.Event()


def mover_tortuga(nombre):
    inicio = time.time()
    progreso = 0
    while not evento_fin.is_set():
        distancia_aleatoria = random.randint(1, 20)  # Distancia aleatoria entre 1 y 20 metros
        progreso += distancia_aleatoria
        print(f"{nombre} ha avanzado {distancia_aleatoria} metros. Progreso total: {progreso} metros.")
        if progreso >= DISTANCIA_META:
            with lock:
                if not evento_fin.is_set():
                    tiempo_total = time.time() - inicio
                    clasificacion.append((nombre, tiempo_total))
                    print(f"¡{nombre} cruza la meta en {tiempo_total:.3f} segundos!")
                    evento_fin.set()
            break
        time.sleep(random.randint(1, 2))  # Pausa aleatoria entre movimientos


def main():
    hilos = []
    for i in range(3):
        hilo = threading.Thread(
            target=mover_tortuga,
            args=(f"Tortuga-{i}",),
            name=f"Worker-{i}"
        )
        hilos.append(hilo)
        hilo.start()

    for hilo in hilos:
        hilo.join()

    print("--------------------------------")
    clasificacion_ordenada = sorted(clasificacion, key=lambda t: t[1])
    if clasificacion_ordenada:
        ganador, tiempo = clasificacion_ordenada[0]
        print(f"Ha ganado la carrera la tortuga: {ganador} con un tiempo de: {tiempo:.3f} segundos.")
    else:
        print("No se completó la carrera.")


if __name__ == "__main__":
    main()
