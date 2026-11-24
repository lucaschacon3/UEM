import threading
import time
import random
import math

# Lista compartida
lista = []

# Lock para controlar la sección crítica
lock = threading.Lock()


def contador(indice, max_val):
    """
    Hilo contador: suma +1 en su posición de la lista
    hasta llegar al valor máximo.
    """
    while lista[indice] < max_val:

        lock.acquire()

        if lista[indice] < max_val:
            lista[indice] = lista[indice] + 1

        lock.release()

        # Dormir entre 2 y 5 segundos
        tiempo = random.randint(2, 5)
        time.sleep(tiempo)


def monitor(max_val, num_hilos):
    """
    Hilo monitor: cada 2 segundos muestra la lista
    y el porcentaje global del progreso.
    """
    total_max = max_val * num_hilos
    terminado = False

    while not terminado:

        lock.acquire()
        copia = lista[:]     # Copia para lectura segura
        lock.release()

        suma_total = sum(copia)

        porcentaje = (suma_total / total_max) * 100
        porcentaje = math.ceil(porcentaje)

        print("Lista:", copia)
        print("Progreso:", porcentaje, "%")
        print("-------------------------------")

        if suma_total >= total_max:
            terminado = True
        else:
            time.sleep(2)


def main():
    num_hilos = 3
    max_val = 10     # En examen podría ser 100

    # Inicializar lista compartida
    for _ in range(num_hilos):
        lista.append(0)

    # Crear hilos contadores
    hilos = []
    for i in range(num_hilos):
        t = threading.Thread(target=contador, args=(i, max_val))
        hilos.append(t)

    # Crear monitor
    monitor_thread = threading.Thread(target=monitor, args=(max_val, num_hilos))

    # Iniciar contadores
    for h in hilos:
        h.start()

    # Iniciar monitor
    monitor_thread.start()

    # Esperar a los hilos contadores
    for h in hilos:
        h.join()

    # Esperar al monitor
    monitor_thread.join()

    print("FIN. Resultado final:", lista)


if __name__ == "__main__":
    main()
