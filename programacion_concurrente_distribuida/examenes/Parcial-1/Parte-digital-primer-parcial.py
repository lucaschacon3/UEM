import threading 
import time
import random
import queue


#Americano - Machiato - Latte
pedidos = ["P1","P2","P3"]
#americano - machiato - latte
#cafe = ["A","B","C"]
cafe = [0,0,0]
tiempos = [0,0,0]
delivery = queue.Queue()

mutex = threading.Lock()

def datafono(i):
        global cafe

        cafeRandom = random.randint(1, 5)

        for b in range(cafeRandom):
            mutex.acquire()
            cafe[i] += 1
            mutex.release()
            time.sleep(random.uniform(0.01, 0.05))



#def cafetera():

hilos = []

for a in range(len(pedidos)):

    hilo = threading.Thread(target=datafono, args=(a,))
    hilos.append(hilo)

for j in hilos:
    j.start()

for k in hilos:
    k.join()
print(f"PEDIDOS => {pedidos}")
print(f"LISTA CAFE =>{cafe}")
