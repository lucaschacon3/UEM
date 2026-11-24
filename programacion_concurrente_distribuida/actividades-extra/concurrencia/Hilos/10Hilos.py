#1) Creamos 10 hilos, q añaden 10 numeros a una lista, un numero cada 10 segundos .
#2) creamos 1 hilo que ordena la lista cada 5 segundos 
#3) cada vez q añadimos un numero , imprimimos la lista antes y despues de añadirlo
#4) al ordenar la lista , la imprimimos tambien antes y despues.

import random
import time
import threading

lista = []
#Candado para protegerlo
mutex = threading.Lock()

def agregar_numero(hilo):
    for i in range(10):
        mutex.acquire()
        try:
            print(f"Hilo {hilo} Antes de añadir => {lista}" )
            numero =random.randint(1,100)
            lista.append(numero)
            print(f"Hilo {hilo} Despues de añadir {numero}:{lista}")
        finally:
            mutex.release()
        time.sleep(10)

def ordenar_lista():
    while True:
        mutex.acquire()
        try:
            print(f"Ordenar :  Antes de ordenar => {lista}")
            #ordenamos la lista
            lista.sort()
            print(f"Ordenar : Despues de ordenar => {lista} ")
        finally:
            mutex.release()
        time.sleep(5)#ordena cada 5 segundos 


def mains():
    hilos_agregar = []

    for i in range(1,11):
        hilo = threading.Thread(target=agregar_numero, args=(i,))
        hilos_agregar.append(hilo)

    hilo_ordenar = threading.Thread(target=ordenar_lista, daemon=True)

    for hilo in hilos_agregar:
        hilo.start()
    hilo_ordenar.start()

    for hilo in hilos_agregar:
        hilo.join()

    print("\nTodos los hilos de añadir han terminando")
    print(f"Lista final => {lista}")

if __name__ == "__main__":
    mains()