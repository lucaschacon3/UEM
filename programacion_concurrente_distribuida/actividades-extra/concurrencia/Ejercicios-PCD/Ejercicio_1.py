#Ejercicio pequeño
#Haz un generador y un cocinero.
#El generador mete 5 tareas en una lista.
#Cada tarea tiene:
#nombre del pedido
#tipo
#tiempo
#El cocinero va sacando una a una y las prepara.
#Sin cliente todavía. Sin cola de entregas todavía. Solo para entender la lista compartida.

import threading
import time 
import random

pedidos = []
tipos = []
tiempos = []

mutex = threading.Lock()
fin = False


def generador():
    global fin 

    for i in range(1,6):
        nombre = "Pedido => " + str(i)

        opcion = random.randint(1,3)

        if opcion == 1:
            tipo = "jamoon"
            tiempo_preparacion = 4
        elif opcion == 2:
            tipo = "queso"
            tiempo_preparacion = 6
        else:
            tipo = "mixto"
            tiempo_preparacion = 8
        mutex.acquire()
        pedidos.append(nombre)
        tipos.append(tipo)
        tiempos.append(tiempo_preparacion)
        mutex.release()
        
        print("GENERADOR añadido :", nombre, tipo,tiempo_preparacion)
        time.sleep(2)
    fin = True

def cocinero():
    trabajando = True

    while trabajando == True:
        nombre = ""
        tipo = ""
        tiempo_preparacion = 0

        mutex.acquire()
        if len(pedidos) > 0 :
            nombre = pedidos.pop(0)
            tipo = tipos.pop(0)
            tiempo_preparacion = tiempos.pop(0)
        mutex.release()

        if nombre != "":
            print ("COCINERO preparando:",nombre,tipo)
            time.sleep(tiempo_preparacion)
            print("COCINERO terminando:",nombre,tipo)
        else:
            if fin == True:
                mutex.acquire()
                vacia = len(pedidos) == 0
                mutex.release()

                if vacia  == True:
                    trabajando = False
            if trabajando == True:
                time.sleep(1)

def main():

    h1 = threading.Thread(target = generador)
    h2 = threading.Thread(target = cocinero)

    h1.start()
    h2.start()

    h1.join()
    h2.join()

    print("Fin del programa")


main()





