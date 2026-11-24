import threading
from time import sleep
from random import randint

def iniciar(nAmigos):
    hilos = []
    for i in range(nAmigos):
        hilos.append(threading.Thread(target = verTemporada, name = "Amigo " + str(i+1)))

    for x in hilos:
        x.start()

    for x in hilos:
        x.join()

def verTemporada():
    global episodios, temporada
    i = 0
    acceso = 0
    vistos = []
    while i < temporada:
        acceso = espera.wait()
        if acceso == 0:
            imprimir(f"Estamos todos listos para ver el episodio {episodios[i]}!")
        sleep(randint(25,30))
        imprimir(threading.current_thread().name + ": He terminado de ver el episodio.")
        vistos.append(episodios[i])
        i+=1
        

def imprimir(mensaje):
    accedido = False
    while not accedido:
        if mutex.acquire(timeout = 2):
            print(mensaje)
            mutex.release()
            accedido = True
        else:
            sleep(1)



nAmigos = int(input("Introduce el numero de amigos: "))
temporada = int(input("Introduce el numero de episodios que van a ver: "))
episodios = []
for i in range(temporada):
    episodios.append("Episodio " + str(i+1))

mutex = threading.Lock()
espera = threading.Barrier(nAmigos)
iniciar(nAmigos)
print("Terminado")