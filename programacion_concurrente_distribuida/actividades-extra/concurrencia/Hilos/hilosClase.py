import random
import time
import threading

#NO USAR FINALLY , WITH ,BREAK, CONTINUE
lista = []

lock = threading.Lock()

def agregar_numero(hilos):

    for i in range(10):
        
        if   lock.acquire():

            print(f"Hilo {hilos} Ante de añadir numero => {lista}" )
            numero = random.randint(1,100)
            lista.append(numero)
            print(f"Hilo {hilos} Despues de añadir numnero =>")
       



        