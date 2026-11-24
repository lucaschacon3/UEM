"""PARPARADID
"""
import threading
import random
import time

PERSONAS = 6
TEMPORADA = 9
episodios = []
vistos = []
amigos = []

barrera = threading.Barrier(PERSONAS)
todosListos = threading.Lock()

def imprimir(mensaje):
    """Funcion q"""
    global todosListos
    impreso = False
    while not impreso:
        if todosListos.acquire(timeout=2):
            print(mensaje)
            todosListos.release
            impreso = True
        else:
            time.sleep(random.randint(1,5))

def ver_episodio(verSerie) :
    """Funcion q"""
    global TEMPORADA
    global episodios
    i = 0
    while i < TEMPORADA:
        barrera.wait()
        imprimir("Empezamos el Capitulo: " + episodios[i])
        time.sleep(random.randint(5,10))
        imprimir("Empezamos el Capitulo: " + episodios[i])
        vistos.append(episodio[i])
        i += 1



for e in range (1, TEMPORADA + 1):
    episodio = "Episodio " + str(e)
    episodios.append(episodio)


for h in range(1, amigos + 1):
    amigo = threading.Thread(target=verSerie, args=["Amigo" + str(i)])
    amigos.append(amigo)