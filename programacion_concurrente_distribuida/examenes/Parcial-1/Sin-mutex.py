import threading
import time
import random
import os

lista = [0,0,0]   # 3 corredores/hilos
mutex = threading.Lock()

def barra(valor, meta):
    # Genera barra de progreso tipo ███░░░
    done = "█" * valor
    left = "░" * (meta - valor)
    return f"{done}{left}"

def contar(i, maxValor):
    global lista

    while lista[i] < maxValor:

        mutex.acquire()
        lista[i] += 1
        mutex.release()

        time.sleep(random.uniform(0.3, 1.2))  # más rápido para visual
        mostrar_carrera(maxValor)

def mostrar_carrera(meta):
    os.system("cls" if os.name == "nt" else "clear")  # limpia consola cada frame

    print("\n🏁  CARRERA DE HILOS EN TIEMPO REAL 🏁\n")

    for i in range(len(lista)):
        print(f" Hilo {i}: {barra(lista[i], meta)}  {lista[i]}/{meta}")

    print("\n" + "-"*40)

def main():
    
    maxValor = 20
    hilos = []

    for i in range(len(lista)):
        h = threading.Thread(target=contar, args=(i,maxValor))
        hilos.append(h)

    for h in hilos:
        h.start()

    for h in hilos:
        h.join()

    mostrar_carrera(maxValor)
    print("\n🏆  RESULTADO FINAL:", lista)

if __name__ == "__main__":
    main()
