import time
import random
import threading

mutex=threading.Lock()
lista=[ ]
tamLista = 5


def inicializarLista(tam):
    hecho = False
    while(not hecho):
        if mutex.acquire(timeout=1):
            for i in range(tam):
                lista.append(" ")
            mutex.release()
            hecho = True
        else:
            print("No he podido adquirir el mutex para inicializar la lista")
"""
          P
[ ][B][C][ ][ ]
    C

       P
[ ][ ][ ][ ][ ]
       C

P
[ ][ ][C][D][E]
       C

P
[A][B][C][D][ ]
C

"""



def productor():
    global lista
    print("Intentando adquirir el mutex")
    for i in range(100):
        if mutex.acquire(timeout=2):
            randomNum = random.randint(1,100)
            lista.append(randomNum)
            print(f"Se ha añadido el numero {randomNum}")
            print(f"la lista se queda como {lista}")
            mutex.release()
            print(f"Hilo 1 ha liberado el mutex")
        time.sleep(random.randint(1,3))


def consumidor():
     global lista
     for i in range(100):
        if mutex.acquire(timeout=2):
            print ("El consumidor ha conseguido el mutex2")
            if len(lista)>0:
                aleatorio = random.randint(0,len(lista)-1)
                lista.pop(aleatorio)
                print(f"Se ha extraido de la posicion {aleatorio}")
                print(f"La lista se queda en {lista}")
            mutex.release()
            print(f"Se ha liberado el mutex 2")


t1 = threading.Thread(target=productor)
t2 = threading.Thread(target=consumidor)

t1.start()
t2.start()

t1.join()
t2.join()
        
