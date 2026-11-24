import threading
from time import sleep
from random import randint

lock = threading.Lock()
lista = []
contador = 0
MAX_VAL = 20

def sumar(i):
    lock.acquire()
    contador = i + 1;

for i in range(MAX_VAL):
    hilo1 = threading.Thread(target=sumar, args=(i,))
    lista.append(hilo1)
    