import threading 
import time
import random
import queue


semaforo = threading.Semaphore(1)


gallinas = ["G1","G2","G3","G4","G5"]
huevos = [0,0,0,0,0]
sinHuevo = [0,0,0,0,0]
criadero = queue.Queue()

def gallina(i):

    diasAño = 365

    for c in range(diasAño):
        prob = random.randint(1,300)/diasAño
        
        semaforo.acquire()
        if prob < 0.18:
            sinHuevo[i] +=1

        else:
            huevos[i] +=1
            if random.random()<0.02:
                criadero.put(0)
        semaforo.release()

        time.sleep(random.uniform(0.01,0.05))


def main():

    hilos =[]

    for  i in range(len(gallinas)):
        hilo = threading.Thread(target = gallina,args=(i,))
        hilos.append(hilo)

    for a in hilos:
        a.start()

    for b in hilos:
        b.join()

    print("gallinas:",gallinas)
    print("huevos por gallina:",huevos)
    print("días sin huevo:",sinHuevo)   
    print("pollitos generados (criadero):",criadero.qsize())


if __name__ == "__main__":
    main()

