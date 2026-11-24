import threading
import random
import time
import queque

huevos = []
noHuevos = []
criadero = queque.Queue()
semHuevos = threading.Semaphore()
semHuevos = threading.Semaphore()

def gallina(numGallina):
    global huevos
    global noHuevos
    global criadero
    for i in range (1,365):
        hayHuevo = random.randint(1, 300)/365
        if hayHuevo < 0.18:
            noHuevos[numGallina] += 1
        else:
            huevos[numGallina] += 1
            esPollo = random.randint(1,300)/300