import time
import threading
import random

matriz = [["P1","parado"],["P2","parado"],["P3","parado"]]
semP1 = threading.Semaphore()
semP2 = threading.Semaphore()
semP3 = threading.Semaphore()
lockPantalla = threading.Lock()

def imprimir(mensaje):
    lockPantalla.acquire()
    print(mensaje,end="")
    lockPantalla.release()

def imprimirMatriz(matriz):
    for i in matriz:
        print(i)
    print()
          

def Proceso1 ():
    global matriz
    while True:
        # semP1.acquire()
        if semP2.acquire(timeout=10):
            matriz[0][1]="-->trabajando"
            time.sleep(random.randint(1,5))
            matriz[0][1]="terminado"
            semP1.release()
        else:
            imprimir("El proceso 1 no ha podido hacer nada. Lo intentamos de nuevo\n\n")

def Proceso3 ():
    while True:
        # semP3.acquire()
        if semP1.acquire(timeout=10):
                matriz[2][1]="-->trabajando"
                time.sleep(random.randint(1,5))
                matriz[2][1]="terminado"
                semP3.release()
        else:
            imprimir("El proceso 3 no ha podido hacer nada. Lo intentamos de nuevo\n\n")

def Proceso2 ():
    while True:
        # semP2.acquire()
        if semP3.acquire(timeout=10):
                matriz[1][1]="-->trabajando"
                time.sleep(random.randint(1,5))
                matriz[1][1]="terminado"
                semP2.release()
        else:
            imprimir("El proceso 2 no ha podido hacer nada. Lo intentamos de nuevo\n\n")


imprimirMatriz(matriz)
print("Empezamos")


hilo1= threading.Thread(target=Proceso1, args=[])
hilo2= threading.Thread(target=Proceso2, args=[])
hilo3= threading.Thread(target=Proceso3, args=[])


hilo1.start()
hilo2.start()
hilo3.start()
# semP1.acquire()
semP2.acquire()
semP3.acquire()

while True:
     imprimirMatriz(matriz)
     time.sleep(2)

hilo1.join()
hilo2.join()
hilo3.join()

print("Terminamos")
