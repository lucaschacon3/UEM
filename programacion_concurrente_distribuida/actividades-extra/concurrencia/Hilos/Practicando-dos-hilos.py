import threading
import time
import random


#Dos hilos
#Añade elemenots, numero o frases etc  a una lista
#Lee siempre el ultimo elemento de una lista
#usando mutex, release, timeout - blocking, acquire
#luego cambiar lista por cola

list = [4]

mutex = threading.Lock()

def añade_elementos():
    for i in range(3):
        list.append(random.randint(1,20))
        time.sleep(1)
        print("Lista ", i , ": ", list)      
    

def leer_ultimo_elemento(lista):
    print("Último elemento de la lista: " , lista[-1])
    time.sleep(0.5)


hilo1 = threading.Thread(target=añade_elementos, args=())
hilo2 = threading.Thread(target=leer_ultimo_elemento, args=(list))


hilo1.start()
hilo2.start()

hilo1.join()
hilo2.join()